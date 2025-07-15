from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Alumni
import pandas as pd
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Import alumni data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the Excel file containing alumni data',
            required=True
        )
        parser.add_argument(
            '--created-by',
            type=str,
            help='Username of the staff member importing the data',
            required=True
        )

    def handle(self, *args, **options):
        file_path = options['file']
        created_by_username = options['created_by']
        
        # Check if file exists
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File not found: {file_path}')
            )
            return
        
        # Get the user who is importing
        try:
            created_by = User.objects.get(username=created_by_username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User not found: {created_by_username}')
            )
            return
        
        # Read Excel file
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading Excel file: {str(e)}')
            )
            return
        
        # Expected columns
        required_columns = [
            'first_name', 'last_name', 'email', 'mobile_number',
            'branch', 'year_of_admission', 'year_of_passout'
        ]
        
        # Check if all required columns are present
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            self.stdout.write(
                self.style.ERROR(f'Missing columns: {", ".join(missing_columns)}')
            )
            self.stdout.write(
                self.style.WARNING(f'Required columns: {", ".join(required_columns)}')
            )
            return
        
        # Optional columns
        optional_columns = [
            'student_id', 'cgpa', 'current_workplace', 'job_title',
            'current_location', 'linkedin_url', 'achievements', 'willing_to_mentor'
        ]
        
        successful_imports = 0
        failed_imports = 0
        skipped_imports = 0
        
        for index, row in df.iterrows():
            try:
                # Check if alumni already exists
                if Alumni.objects.filter(email=row['email']).exists():
                    self.stdout.write(
                        self.style.WARNING(f'Alumni with email {row["email"]} already exists. Skipping.')
                    )
                    skipped_imports += 1
                    continue
                
                # Create alumni data
                alumni_data = {
                    'first_name': str(row['first_name']).strip(),
                    'last_name': str(row['last_name']).strip(),
                    'email': str(row['email']).strip().lower(),
                    'mobile_number': str(row['mobile_number']).strip(),
                    'branch': str(row['branch']).strip(),
                    'year_of_admission': int(row['year_of_admission']),
                    'year_of_passout': int(row['year_of_passout']),
                    'created_by': created_by
                }
                
                # Add optional fields if present
                for col in optional_columns:
                    if col in df.columns and pd.notna(row[col]):
                        if col == 'cgpa':
                            alumni_data[col] = float(row[col])
                        elif col == 'willing_to_mentor':
                            alumni_data[col] = bool(row[col])
                        else:
                            alumni_data[col] = str(row[col]).strip()
                
                # Create alumni record
                alumni = Alumni.objects.create(**alumni_data)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully imported: {alumni.full_name}')
                )
                successful_imports += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error importing row {index + 1}: {str(e)}')
                )
                failed_imports += 1
                continue
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(f'\nImport Summary:')
        )
        self.stdout.write(f'Successful imports: {successful_imports}')
        self.stdout.write(f'Failed imports: {failed_imports}')
        self.stdout.write(f'Skipped imports: {skipped_imports}')
        self.stdout.write(f'Total rows processed: {len(df)}')
        
        # Create a sample Excel file for reference
        sample_file = 'alumni_import_sample.xlsx'
        sample_data = {
            'first_name': ['John', 'Jane'],
            'last_name': ['Doe', 'Smith'],
            'email': ['john.doe@example.com', 'jane.smith@example.com'],
            'mobile_number': ['9876543210', '9876543211'],
            'branch': ['Electronics Engineering', 'Computer Engineering'],
            'year_of_admission': [2018, 2019],
            'year_of_passout': [2022, 2023],
            'student_id': ['EE18001', 'CE19001'],
            'cgpa': [8.5, 9.0],
            'current_workplace': ['Tech Corp', 'Data Inc'],
            'job_title': ['Software Engineer', 'Data Scientist'],
            'current_location': ['Mumbai', 'Bangalore'],
            'linkedin_url': ['https://linkedin.com/in/johndoe', 'https://linkedin.com/in/janesmith'],
            'achievements': ['Best Project Award', 'Scholarship Recipient'],
            'willing_to_mentor': [True, False]
        }
        
        sample_df = pd.DataFrame(sample_data)
        sample_df.to_excel(sample_file, index=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSample Excel file created: {sample_file}')
        )
