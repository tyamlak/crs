from django.shortcuts import render
from case.models import Case, CaseCategory
from datetime import datetime
import calendar 
from django.contrib.auth.decorators import login_required


def create_pdf(table_data=None,ex_table=None, filename='CrimeReport.pdf', title=''):
    if not table_data:
        return 'Error: Table Data not provided.'
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import TableStyle
    from reportlab.lib import colors
    from reportlab.platypus import Table
    from reportlab.lib.styles import getSampleStyleSheet

    pdf = SimpleDocTemplate(
        filename,
        pagesize=letter
    )
    pdf.title = title
    table = Table(table_data)
    styles = getSampleStyleSheet()
    header = styles['Heading1']

    p = Paragraph(title, header)
    p_break = Paragraph("",header)

    style = TableStyle(
        [
            ('BACKGROUND', (0, 0), (4, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]
    )
    table.setStyle(style)

    rowNumb = len(table_data)
    for i in range(1, rowNumb):
        if i%2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige
        ts = TableStyle(
            [
                ('BACKGROUND', (0,i), (-1,i), bc),
            ]
        )
        table.setStyle(ts)
    
    ts = TableStyle(
        [
            ('BOX', (0,0), (-1,-1),2,colors.black),
        ]
    )
    table.setStyle(ts)

    new_table = None
    if ex_table:
        new_table = Table(ex_table)
        new_table.setStyle(style)
        new_table.setStyle(ts)

    elems = []
    elems.append(p)
    elems.append(p_break)
    elems.append(table)
    elems.append(p_break)
    elems.append(Paragraph("Crime Stats based on severity", header))
    elems.append(p_break)
    elems.append(new_table)
    pdf.build(elems)


def quarterly_report_data():
    table_data = []
    month_list = []
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    description = "Quarterly report for: "
    for i in range(3):
        current_month -= 1
        if current_month == 0:
            current_month = 12
            current_year -= 1
        month_list.append((current_month, current_year))
    month_names = ['']
    print("Month list: ")
    for (m, y) in month_list:
        month_name = calendar.month_name[m]
        month_names.append(month_name)
        description += f'{month_name} {y}, '
    table_data.append(month_names)
    case_set = Case.objects.all()
    for ct in CaseCategory.objects.all():
        table_row = []
        table_row.append(ct.crime)
        print(ct.crime, " Crime for month and year ")
        for (m, y) in month_list:
            crime_count = case_set.filter(
                category=ct, date_created__month=m, date_created__year=y).count()
            table_row.append(crime_count)
        table_data.append(table_row)
    return table_data, description.strip(',')


def monthly_report_data():
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    report_month = current_month - 1
    if report_month == 0:
        report_month = 12
        current_year -= 1
    month_name = calendar.month_name[report_month]
    table_data = []
    table_data.append(['','Week 1','Week 2','Week 3','Week 4'])
    case_set = Case.objects.filter(date_created__year=current_year,date_created__month=report_month)
    for ct in CaseCategory.objects.all():
        table_row = []
        _cases = case_set.filter(category=ct)
        if True:
            table_row.append(ct.crime)
            table_row.append(case_set.filter(category=ct,date_created__day__in=range(1,8)).count())
            table_row.append(case_set.filter(category=ct,date_created__day__in=range(8,15)).count())
            table_row.append(case_set.filter(category=ct,date_created__day__in=range(15,23)).count())
            table_row.append(case_set.filter(category=ct,date_created__day__in=range(23,30)).count())
        table_data.append(table_row)
    return table_data, f'Monthly Report for: {month_name} {current_year} '


def yearly_report_data():
    current_year = datetime.utcnow().year
    report_year = current_year - 1
    table_data = []
    table_data.append(["","Number of cases"])
    case_set = Case.objects.filter(date_created__year=report_year)
    for i in range(1,13):
        table_row = []
        table_row.append(calendar.month_name[i])
        table_row.append(case_set.filter(date_created__month=i).count())
        table_data.append(table_row)
    return table_data

def yearly_crime_report():
    current_year = datetime.utcnow().year
    report_year = current_year - 1
    table_data = []
    table_data.append(["","Severe","Medium","Light"])
    case_set = Case.objects.filter(date_created__year=report_year)
    for i in range(1,13):
        table_row = []
        table_row.append(calendar.month_name[i])
        for ct in ('S','M','L'):
            table_row.append(case_set.filter(date_created__month=i,category__crime_type=ct).count())
        table_data.append(table_row)
    return table_data, f'Yearly Number of cases for {report_year} '

@login_required
def report(request):
    from case.models import Report
    from django.core.files.base import File
    error = ''
    report_type = 1
    file_name = ''
    if request.POST:
        table_data = None
        try:
            report_type = int(request.POST.get('report_type'))
        except Excecption as e:
            print('Error parsing int from request')
        if report_type == 0:
            file_name = "Monthly Crime-Report.pdf"
            table_data, description = monthly_report_data()
            create_pdf(table_data,filename=file_name,title=description)
        elif report_type == 1:
            file_name = "Quarterly Crime-Report.pdf"
            table_data, description = quarterly_report_data()
            create_pdf(table_data,filename=file_name,title=description)
        elif report_type == 2:
            file_name = "YearlyReport.pdf"
            table_data = yearly_report_data()
            ex_table, description = yearly_crime_report()
            create_pdf(table_data,ex_table=ex_table,filename=file_name,title=description)
        f = open(file_name,'rb')
        report_file = File(f)
        Report(file=report_file).save()
        return render(request,'case/report.html',{
        })
    report_set = Report.objects.all()
    return render(
        request, 'case/report.html', {
            'error': error,'report_set':report_set,
        }
    )
