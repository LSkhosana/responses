COMMON_QUESTIONS = [
    {"key":"common_easy_use","section":"Your experience with Medworkflow","text":"Medworkflow is easy to use for my day-to-day responsibilities.","type":"likert","required":True},
    {"key":"common_information","section":"Your experience with Medworkflow","text":"The system provides the information I need to complete my work.","type":"likert","required":True},
    {"key":"common_manual_work","section":"Your experience with Medworkflow","text":"Medworkflow has reduced unnecessary manual work.","type":"likert","required":True},
    {"key":"common_workflow","section":"Your experience with Medworkflow","text":"Medworkflow has improved my workflow compared with the previous process.","type":"likert","required":True},
    {"key":"common_confidence","section":"Your experience with Medworkflow","text":"I feel confident using the Medworkflow functions required for my role.","type":"likert","required":True},
    {"key":"common_training","section":"Training & support","text":"The training I received prepared me to use Medworkflow effectively.","type":"likert","required":True},
    {"key":"common_support","section":"Training & support","text":"When I need assistance with Medworkflow, I can get the support I need.","type":"likert","required":True},
    {"key":"common_resolution","section":"Training & support","text":"Problems I report are addressed effectively.","type":"likert","required":True},
    {"key":"training_more","section":"Training & support","text":"Do you feel you would benefit from additional Medworkflow training?","type":"single","options":["Yes","No","Unsure"],"required":True},
    {"key":"training_topics","section":"Training & support","text":"What would you like additional training on?","type":"text","show_if":{"key":"training_more","value":"Yes"}},
    {"key":"improved_most","section":"Final feedback","text":"What has improved the most since the new Medworkflow workflow was introduced?","type":"textarea"},
    {"key":"frustration","section":"Final feedback","text":"What currently causes you the most frustration or unnecessary work?","type":"textarea"},
    {"key":"improve_one","section":"Final feedback","text":"If we could improve one thing about Medworkflow or the way it is supported, what should it be?","type":"textarea"},
]

SURVEYS = {
"admissions":{"title":"Admissions Workflow Review","description":"Tell us how the current admissions workflow is performing and where it can be improved.","questions":[
{"key":"usage","section":"Your workflow","text":"How frequently do you use Medworkflow for patient admissions?","type":"single","options":["Daily","Several times a week","Weekly","Less often"],"required":True},
{"key":"case_available","section":"Your workflow","text":"When a scheduled theatre patient arrives, how often is their case already available in Medworkflow?","type":"frequency","required":True},
{"key":"case_complete","section":"Your workflow","text":"When the case is available, how often does it contain enough information for you to complete the admission without obtaining additional information?","type":"frequency","required":True},
{"key":"info_correct","section":"Your workflow","text":"What information do you most commonly have to add or correct?","type":"multi","options":["Patient details","Medical aid","Authorisation","Doctor","Procedure","Theatre details","Other","Usually nothing"]},
{"key":"create_pre_admission","section":"Your workflow","text":"How often do you still have to create a pre-admission yourself for a scheduled theatre patient?","type":"often","required":True},
{"key":"create_theatre_case","section":"Your workflow","text":"How often do you still have to create a theatre case yourself for a scheduled theatre patient?","type":"often","required":True},
{"key":"case_rework_reason","section":"Your workflow","text":"When you have to create or substantially complete a case yourself, what are the usual reasons?","type":"multi","options":["Case wasn't created by Doctor Rooms","Late addition","Missing information","Incorrect information","Case not visible","Walk-in or emergency","System problem","Other"]},
{"key":"trimed_available","section":"Trimed","text":"How often is information captured in Medworkflow correctly available in Trimed without you having to capture it again?","type":"frequency","required":True},
{"key":"trimed_reentry","section":"Trimed","text":"How often do you manually re-enter information in Trimed that has already been captured in Medworkflow?","type":"often","required":True},
{"key":"trimed_fields","section":"Trimed","text":"What information, if any, most commonly requires manual entry or correction in Trimed?","type":"text"},
{"key":"trimed_fallback","section":"Trimed","text":"Have you had to admit a patient directly through Trimed because you could not complete the admission through Medworkflow?","type":"single","options":["Yes","No"],"required":True},
{"key":"trimed_fallback_reason","section":"Trimed","text":"Why did you need to use Trimed?","type":"textarea","show_if":{"key":"trimed_fallback","value":"Yes"}},
{"key":"trimed_sync_back","section":"Trimed","text":"Did the admission subsequently appear correctly in Medworkflow?","type":"single","options":["Yes","No","Unsure"],"show_if":{"key":"trimed_fallback","value":"Yes"}}
]},
"doctor-rooms":{"title":"Doctor Rooms / Doctor Dashboard Review","description":"Tell us how well Medworkflow supports the beginning of the patient journey and theatre booking process.","questions":[
{"key":"usage","section":"Creating the patient journey","text":"How frequently do you use the Medworkflow Doctor Dashboard?","type":"single","options":["Daily","Several times a week","Weekly","Less often"],"required":True},
{"key":"patient_capture_easy","section":"Creating the patient journey","text":"How easy is it to find an existing patient or capture a new patient in Medworkflow?","type":"ease","required":True},
{"key":"case_create_easy","section":"Creating the patient journey","text":"How easy is it to create and submit a theatre case?","type":"ease","required":True},
{"key":"fields_clear","section":"Creating the patient journey","text":"Are the fields and information required when creating a theatre case clear to you?","type":"frequency","required":True},
{"key":"difficult_parts","section":"Creating the patient journey","text":"Which parts of creating a patient or theatre case cause you the most difficulty?","type":"multi","options":["Finding patient","Patient details","Medical aid","Procedure","Theatre date","Doctor information","Other","None"]},
{"key":"without_help","section":"Creating the patient journey","text":"How often are you able to complete the patient and theatre case in Medworkflow without needing assistance from hospital staff?","type":"frequency","required":True},
{"key":"outside_method","section":"Workflow adoption","text":"How often do you still send theatre booking information outside Medworkflow?","type":"often","required":True},
{"key":"outside_reason","section":"Workflow adoption","text":"Why do you still use another method?","type":"multi","options":["System problem","Medworkflow is slower","Missing functionality","Unsure how to complete the process","Hospital staff requested it","Urgent or late case","Other"]},
{"key":"case_not_appear","section":"Workflow adoption","text":"How often have cases you created successfully not appeared correctly for the hospital/theatre team?","type":"often","required":True},
{"key":"workflow_change","section":"Workflow adoption","text":"Compared with the previous paper/email-based process, how has Medworkflow affected submitting a patient for theatre?","type":"change","required":True}
]},
"theatre":{"title":"Theatre Management Workflow Review","description":"Tell us how well Medworkflow supports theatre list management, changes and coordination.","questions":[
{"key":"usage","section":"Theatre list","text":"How frequently do you use Medworkflow to manage theatre cases/lists?","type":"single","options":["Daily","Several times a week","Weekly","Less often"],"required":True},
{"key":"cases_appear","section":"Theatre list","text":"How often do theatre cases created by Doctor Rooms appear correctly on the theatre list?","type":"frequency","required":True},
{"key":"cases_complete","section":"Theatre list","text":"How often is information received from Doctor Rooms complete enough to manage the case without contacting them for additional information?","type":"frequency","required":True},
{"key":"correct_info","section":"Theatre list","text":"What information do you most commonly have to correct or obtain?","type":"multi","options":["Patient information","Doctor","Procedure","Theatre date/time","Medical aid","Other","Usually nothing"]},
{"key":"manual_add","section":"Theatre list","text":"How often do you have to manually add a theatre case that should already have been created upstream?","type":"often","required":True},
{"key":"reorder_easy","section":"Theatre list","text":"How easy is it to reorder or move cases when organising the theatre list?","type":"ease","required":True},
{"key":"late_change_easy","section":"Theatre list","text":"How easy is it to handle late additions or changes using Medworkflow?","type":"ease","required":True},
{"key":"excel_export","section":"Theatre list","text":"Does the Excel export provide the information you need for the theatre list?","type":"single","options":["Always","Usually","Sometimes","Rarely","Never","I don't use the export"],"required":True},
{"key":"outside_info","section":"Workflow","text":"How often do you still maintain or distribute theatre information outside Medworkflow?","type":"often","required":True},
{"key":"outside_reason","section":"Workflow","text":"Why is another method still required?","type":"multi","options":["Missing functionality","Reliability concerns","Information incomplete","Staff preference","Existing hospital process","Urgent changes","Other"]},
{"key":"work_change","section":"Workflow","text":"Compared with the previous process of receiving bookings and manually maintaining the theatre list, how has Medworkflow affected the amount of work required?","type":"work_change","required":True}
]}
}

OPTIONS = {
"likert":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"],
"frequency":["Almost always","Often","Sometimes","Rarely","Never"],
"often":["Never","Rarely","Sometimes","Often","Very often"],
"ease":["Very difficult","Difficult","Neither difficult nor easy","Easy","Very easy"],
"change":["Much worse","Worse","No significant change","Better","Much better"],
"work_change":["Much more work","More work","No significant change","Less work","Much less work"]
}

def get_survey(slug):
    survey = SURVEYS.get(slug)
    if not survey:
        return None
    return {**survey, "slug":slug, "questions":survey["questions"] + COMMON_QUESTIONS}
