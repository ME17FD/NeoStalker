from io import StringIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import PdfUploadForm
import tabula
import pandas as pd
import os
from django.contrib.auth.decorators import login_required

@login_required()  
def pdf_to_excel(request):
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'pdf_file' not in request.FILES:
            return render(request, 'upload.html', {'error': 'No file uploaded.'})

        try:
            # Get the uploaded file
            pdf_file = request.FILES['pdf_file']

            # Save the file temporarily
            file_name = default_storage.save(pdf_file.name, ContentFile(pdf_file.read()))

            # Extract tables from the PDF using Tabula
            dfs = tabula.read_pdf(default_storage.path(file_name), pages='all', multiple_tables=True) # type: ignore

            if not dfs:
                # Handle case where no tables are found in the PDF
                error_message = "No tables found in the uploaded PDF."
                return render(request, 'upload.html', {'error': error_message})

            # Combine all DataFrames into one
            df = pd.concat(dfs, ignore_index=True)

            # Store the DataFrame and file name in the session for further processing
            request.session['pdf_data'] = df.to_json()
            request.session['pdf_filename'] = file_name

            # Clean up: Delete the temporary PDF file
            default_storage.delete(file_name)

            # Redirect to the column renaming page
            return redirect('rename_columns')

        except Exception as e:
            # Handle any errors during PDF processing
            error_message = f"An error occurred while processing the PDF: {str(e)}"
            return render(request, 'upload.html', {'error': error_message})

    return render(request, 'upload.html')


@login_required()  
def rename_columns(request):
    if 'pdf_data' not in request.session:
        return redirect('pdf_to_excel')

    pdf_data = request.session['pdf_data']
    df = pd.read_json(StringIO(pdf_data))
    pdf_filename = request.session['pdf_filename']
    df.astype(str)

    if request.method == 'POST':
        # Get the original column names and indices
        original_columns = list(df.columns)
        original_indices = [int(idx) for idx in request.POST.getlist('original_indices')]

        # Get columns marked for removal
        columns_to_remove = request.POST.getlist('columns_to_remove')
        if columns_to_remove:
            df.drop(columns=columns_to_remove, inplace=True)

        # Collect new column names using original indices
        new_columns = {}
        for idx in original_indices:
            original_column = original_columns[idx]
            if original_column not in columns_to_remove:  # Only process columns not removed
                new_name = request.POST.get(f'column_{idx}')
                if new_name and new_name.strip():
                    new_columns[original_column] = new_name.strip()

        # Rename columns
        df.rename(columns=new_columns, inplace=True)

        # Save and return the Excel file
        excel_path = pdf_filename.replace(".pdf", ".xlsx")
        df.to_excel(excel_path, index=False)
        with open(excel_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename={excel_path}'
            return response

    return render(request, 'rename_columns.html', {'columns': df.columns})