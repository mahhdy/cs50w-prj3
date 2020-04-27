import csv
from orders.models import Employee,Title,Team,Agency,Shift
from django.utils import timezone, dateformat
from django.contrib.auth.models import User
def nw():
    return dateformat.format(timezone.now(),"d-M H:i:s")
def run():
    print(f'Script Started at {nw()}')
    fhand = open('.csv')
    reader = csv.reader(fhand)
    # Title.objects.all().delete()
    # Agency.objects.all().delete()
    # Team.objects.all().delete()
    # Shift.objects.all().delete()
    for u in reader:
        # User.objects.filter(username=u[0]).update(is_active=bool(u[4]))
        # User.objects.create_user(username=u[0],password=u[3],first_name=u[1],last_name=u[2],is_staff=True)
        # Team.objects.filter(name=u[0]).update(team_type=u[1])
        # a, created=Title.objects.get_or_create(name=u[5].title())
        # b, created=Agency.objects.get_or_create(name=u[9].title())
        # c, created=Team.objects.get_or_create(name=u[6].title())
        # d, created=Shift.objects.get_or_create(name=u[10].title())
        # a0=None
        # if len(u[8]):a0=u[8]
        # e=Employee(first_name=u[1].lower(),last_name=u[2].lower(),nick_name=u[3].lower()
        #     ,badge=u[0],touch=u[4].lower(),position=a,team=c,start=u[7],end=a0,agency=b,shift=d,days=u[11].lower())
        # e.save()

    print(f'Script Finished at {nw()}')