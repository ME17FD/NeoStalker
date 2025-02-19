from django.db.models import Q
from .models import person 
from django.contrib import messages
import pandas as pd
import logging
import tabula 


logger = logging.getLogger(__name__)


def pdf_to_excel(pdf_file_path):
    try:
        tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, encoding='latin-1')  
        
        # Check if any tables were extracted
        if not tables:
            print("No tables found in the PDF.")
            return None
        
        excel_file_path = pdf_file_path + ".xlsx"
        with pd.ExcelWriter(excel_file_path) as writer:
            for i, table in enumerate(tables):
                if isinstance(table, pd.DataFrame):
                    table.to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)        
        print(f"Excel file saved successfully at {excel_file_path}")
        return excel_file_path
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
COLUMN_MAPPING = {
    'nom': 'lname',
    'prenom': 'fname',
    'prénom': 'fname',
    'date': 'bday',
    'email': 'email',
    'tel': 'phone',
    'cin': 'cin',
    'cne': 'cen',
    'massar': 'cen',
    'last name': 'lname',
    'first name': 'fname',
    'birthday': 'bday',
    'phone number': 'phone',
}


def process_excel_file(request, file_path: str, filename: str) -> None:
    """
    Reads an Excel file with multiple sheets and processes each row.
    """

    try:
        # Read all sheets into a dictionary of DataFrames
        sheet_data = pd.read_excel(file_path, sheet_name=None)

        total_created = 0
        total_updated = 0

        for sheet_name, df in sheet_data.items():
            if df.empty:
                logger.info(f"Skipping empty sheet: {sheet_name}")
                continue  # Skip empty sheets

            df.dropna(how='all', inplace=True)  # Remove fully empty rows
            df.columns = [col.strip().lower() for col in df.columns]

            # Find valid columns in this sheet
            valid_columns = set(df.columns) & set(COLUMN_MAPPING.keys())
            if not valid_columns:
                logger.warning(f"Skipping sheet '{sheet_name}': No valid columns found.")
                continue  # Skip sheets without valid columns

            logger.info(f"Processing sheet: {sheet_name} with valid columns: {valid_columns}")

            created_count = 0
            updated_count = 0

            # Filter rows that have at least one non-null valid column
            for _, row in df.iterrows():
                created = prepare_person_object(row, filename)
                # Increment the appropriate counter
                if created==True:
                    created_count += 1
                else:
                    updated_count += 1

            total_created += created_count
            total_updated += updated_count
            
        messages.success(request, f"total created :{total_created}")
        messages.success(request, f"total updated :{total_updated}")
        print(f'total created :{total_created}')
        print(f'total updated :{total_updated}')
        if total_created == 0 and total_updated == 0:
            messages.error(request, "No valid data found in any sheet.")

    except Exception as e:
        logger.error(f"Error processing Excel file: {e}")
        messages.error(request, "An error occurred while processing the Excel file.")
        raise

def prepare_person_object(row, filename: str) ->  bool|None:
    """
    Prepares a person object for creation or update based on the row data.
    Returns a tuple of (person_object, created), where `created` is a boolean.
    """
    # Normalize column names to lowercase and map them to standardized field names
    normalized_row = {COLUMN_MAPPING.get(key.lower(), key): value for key, value in row.items()}

    # Define default fields
    defaults = {
        'ismale': False,
        'bday': normalized_row.get('bday', None),
        'email': str(normalized_row.get('email', '')).strip(),
        'phone': str(normalized_row.get('phone', '')).strip(),
        'cin': str(normalized_row.get('cin', '')).strip(),
        'cen': str(normalized_row.get('cen', '')).strip(),
    }

    # Add all unrecognized fields to the `info` field in a "field: value" format
    info_fields = []
    for field, value in normalized_row.items():
        if field not in defaults and pd.notna(value):  # Exclude fields already in defaults
            info_fields.append(f"{field}: {str(value).strip()}")
    
    # Add filename to the `info` field
    info_fields.append(f"filename: {filename}")
    
    # Combine all info fields into a single string
    defaults['info'] = "\n".join(info_fields)
    
    # Normalize name fields for case-insensitive matching
    
    lname = str(normalized_row.get('lname', '')).strip()
    fname = str(normalized_row.get('fname', '')).strip()
    
    # Check if a person with the same first and last name exists (case-insensitive)
    person_obj, created = person.objects.get_or_create(
        lname=lname,  # Case-insensitive match for last name
        fname=fname,  # Case-insensitive match for first name
        defaults=defaults
    )
    if lname or fname:  
        if not created:
            # Update fields if they have changed
            updated = update_person_fields(person_obj, defaults)
            if updated:
                person_obj.save()
    else:
        return None
    
    return created


def update_person_fields(person_obj:person, defaults: dict) -> bool:
    """
    Updates the person object fields if they differ from the defaults.
    Returns True if any field was updated, otherwise False.
    """
    updated = False
    
    if person_obj.bday != defaults['bday'] and defaults['bday']:
        person_obj.bday = defaults['bday']
        updated = True
    
    if person_obj.email != defaults.get('email') and defaults.get('email') and str(defaults.get('email')) not in str(person_obj.email) :
        person_obj.email += "\n" + defaults['email']
        updated = True
    
    if person_obj.phone != defaults.get('phone') and defaults.get('phone') and str(defaults.get('phone')) not in str(person_obj.phone):
        person_obj.phone += "\n" + defaults['phone']
        updated = True
    
    if person_obj.cin != defaults.get('cin') and defaults.get('cin'):
        person_obj.cin = defaults['cin']
        updated = True
    
    if person_obj.cen != defaults.get('cen') and defaults.get('cen'):
        person_obj.cen = defaults['cen']
        updated = True
    
    if defaults['info'] and defaults['info'] not in person_obj.info  and defaults['info'] :
        person_obj.info += "\n" + defaults['info']
        updated = True
    person_obj.save()
    return updated
