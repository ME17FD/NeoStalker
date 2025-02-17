from sys import exception
from django.core.management.base import BaseCommand
import pandas as pd
from myapp.models import person

class Command(BaseCommand):
    help = 'Transfer data from Excel to database'

    def add_arguments(self, parser):
        parser.add_argument(
        "--delete_old",  # Optional argument
        action="store_true",
        default=False,  # Default to False
        help="Flag to delete old data"
        )
        parser.add_argument(
        "--excel_file",  # Optional argument for the Excel file
        type=str,  # Expecting a string (file path)
        default="xlx/ex.xlsx",  # Default file name/path if not provided
        help="Path to the Excel file"
        )


    def handle(self, *args, **options):
        self.stdout.write('Starting data transfer...')

        
        if options.get('delete_old'):
            nb_dl = person.objects.all().count()
            delete_list= person.objects.all().delete()

            print(f'{nb_dl} deleted from database')
            return
        
        
        # Load data from Excel into a DataFrame
        excel_file = options.get('excel_file')
        df = pd.read_excel(excel_file)
        df.columns = df.columns.str.lower()

        # Initialize a counter for errors
        errors = 0
        created_c =0
        update_c = 0
        duplicate_c=0
        # Iterate through the rows and process data
        for index, row in df.iterrows():
            fname = row.get('nom', '')
            lname = row.get('prenom', '')
            cin = row.get('cin', '')
            cne = row.get('cne', '')
            info = row.get('info', '') +'\n'+ str(excel_file).split('\\')[-1]
            email = row.get('email', '')
            
            if not pd.isna(email) and '@' not in email:
                email = ''

            # Create or update the Person object
            try:
                person_obj, created = person.objects.get_or_create(
                    fname=fname, lname=lname, cin=cin,
                    defaults={
                        'ismale': True,  # Default values for new objects
                        'email': email,
                        'phone': '',
                        'cen': cne,
                        'info': info,
                        'bday': '',
                    }
                )
                if not created:  # If the person already exists
                    if info and (info not in person_obj.info):
                        person_obj.info += '\n' + info
                        person_obj.save()
                        update_c +=1
                    else:
                        if info !='' : duplicate_c +=1

                else:
                    created_c +=1
            except Exception as e:
                self.stdout.write(f'Error processing row {index}: {e}')
                errors += 1

        # Output the number of errors encountered
        self.stdout.write(f'Total number profiles created: {created_c}')
        self.stdout.write(f'Total number profiles updated: {update_c}')
        self.stdout.write(f'Total number duplicates found: {duplicate_c}')
        self.stdout.write(f'Total number of errors: {errors}')
        self.stdout.write("Data transferred to database successfully.")
