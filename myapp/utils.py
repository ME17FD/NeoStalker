from django.db.models import Q
from .models import person 
from django.contrib import messages


def create_or_update(request,row, filename: str = '') -> None:
    try:
        defaults={
                'ismale': False,
                'bday': row.get('Date', None),
                'email': row.get('Email', ''),
                'phone': row.get('tel', ''),
                'cin': row.get('CIN', ''),
                'cen': row.get('CNE', ''),
                'info': row.get('info', '') + "\n" + " ".join(filename.split(".")[0:-1])
            }
        # Check if a person with the same first and last name exists
        person_obj, created = person.objects.get_or_create(
            lname=row.get('Nom', '').strip(),
            fname=row.get('Prenom', '').strip(),
            defaults=defaults
        )

        if created:
            messages.success(request, f"New person added: {person_obj.fname} {person_obj.lname}")
            return
        if person_obj.bday != defaults['bday'] and defaults['bday']:
            person_obj.bday = defaults['bday']
            updated = True

        if person_obj.email != defaults.get('email') and defaults.get('email'):
            person_obj.email += "\n" + defaults['email']
            updated = True

        if person_obj.phone != defaults.get('phone') and defaults.get('phone'):
            person_obj.phone += "\n" + defaults['phone']
            updated = True

        if person_obj.cin != defaults.get('cin') and defaults.get('cin'):
            person_obj.cin = defaults['cin']
            updated = True

        if person_obj.cen != defaults.get('cen') and defaults.get('cen'):
            person_obj.cen = defaults['cen']
            updated = True
            if defaults['info']:
                if defaults['info'] not in person_obj.info:
                    person_obj.info += "\n" + defaults['info']
                    updated = True
            
        if updated:
            person_obj.save()
            messages.info(request, f"Updated details for {person_obj.fname} {person_obj.lname}")

    except Exception as e:
        print(f"Error processing row: {e}")
        messages.error(request, f"Error processing row: {e}")
    
