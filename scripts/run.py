import csv
from orders.models import Topping,Food,Food_type
from django.utils import timezone, dateformat
# from django.contrib.auth.models import User
def nw():
    return dateformat.format(timezone.now(),"d-M H:i:s")
def run():
    print(f'Script Started at {nw()}')
    fhand = open('db.csv')
    reader = csv.reader(fhand)
    # Title.objects.all().delete()
    # Agency.objects.all().delete()
    # Team.objects.all().delete()
    # Topping.objects.all().delete()
    
    # for u in reader:
    for u in range(50,68):    
        # f, created=Food_type.objects.get_or_create(name=u[2])
        # User.objects.filter(username=u[0]).update(is_active=bool(u[4]))
        # User.objects.create_user(username=u[0],password=u[3],first_name=u[1],last_name=u[2],is_staff=True)
        # Team.objects.filter(name=u[0]).update(team_type=u[1])
        # a, created=Food.objects.get_or_create(name=u[0],size=u[1],food_type =f,topping_count =u[3],accepts_extra =u[4],price=u[5])
        # b, created=Agency.objects.get_or_create(name=u[9].title())
        # c, created=Team.objects.get_or_create(name=u[6].title())
        # d, created=Shift.objects.get_or_create(name=u[10].title())
        # a0=None
        # if len(u[8]):a0=u[8]
        # e=Employee(first_name=u[1].lower(),last_name=u[2].lower(),nick_name=u[3].lower()
        #     ,badge=u[0],touch=u[4].lower(),position=a,team=c,start=u[7],end=a0,agency=b,shift=d,days=u[11].lower())
        # e.save()
        Food.objects.filter(pk=u).update(accepts_extra=False)
    print(f'Script Finished at {nw()}')