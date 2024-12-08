import datetime
from dateutil import relativedelta

def load_date():
	with open("date", "r") as f:
		date_on_file = datetime.date(*[int(n) for n in f.read().split(" ")])
		# print(date_on_file.strftime("%A %d %b %YAF"))
	return(date_on_file)

def save_date(date):
	with open("date", "w") as f:
		f.write(date.strftime("%Y %m %d"))

def add_time(date_before, n_days=0, n_weeks=0, n_months=0):
	new_date = date_before + datetime.timedelta(days=(n_days+7*n_weeks))
	new_date += relativedelta.relativedelta(months=n_months)
	save_date(new_date)
	return(new_date)

def set_date(d, m, y):
	save_date(datetime.date(int(y), int(m), int(d)))

if __name__ == "__main__":
	date = load_date()
	date_before = load_date()
	print(date.strftime("%A %d %b %YAF"))
	print("adding 4 days")
	date = add_time(date, n_days=4, n_weeks=0, n_months=0)
	print(date.strftime("%A %d %b %YAF"))
	print("adding a week and a day")
	date = add_time(date, n_days=1, n_weeks=1, n_months=0)
	print(date.strftime("%A %d %b %YAF"))
	print("adding a month")
	date = add_time(date, n_days=0, n_weeks=0, n_months=1)
	print(date.strftime("%A %d %b %YAF"))
	save_date(date_before)

