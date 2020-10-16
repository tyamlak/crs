def get_criminal_form_data(request,method='POST'):
    form_data = getattr(request,method)
    f_name = form_data.get('C_fname')
    m_name = form_data.get('C_mname')
    l_name = form_data.get('C_lname')
    age = form_data.get('C_age')
    sex = form_data.get('C_sex')
    dob = form_data.get('C_date_of_birth')
    pob = form_data.get('C_place_of_birth')
    nationality = form_data.get('C_nationality')
    ethnicity = form_data.get('C_ethnicity')
    religion = form_data.get('C_religion')
    income = form_data.get('C_income')
    phone_number = form_data.get('C_phone_number')
    work_type = form_data.get('C_work_type')
    work_address = form_data.get('C_work_address')
    work_role = form_data.get('C_work_role')
    salary = form_data.get('C_salary')
    return {
        'f_name':f_name,'m_name':m_name,'l_name':l_name,
        'age':age,'sex':sex,'dob':dob,'pob':pob,
        'nationality':nationality,'ethnicity':ethnicity,
        'religion':religion,'income':income,'phone_number':phone_number,
        'work_type':work_type,'work_address':work_address,'work_role':work_role,
        'salary':salary,
    }