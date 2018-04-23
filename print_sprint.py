from taiga import TaigaAPI
from xhtml2pdf import pisa
from datetime import date
import jinja2
import inquirer

sourceHtml=''
outputFilename=''

# Utility function
def convertHtmlToPdf():
    

    questions = [
        inquirer.Text('host', message="your taiga api host"),
        inquirer.Text('user', message="your taiga username"),
        inquirer.Password('password', message="your taiga password"),    ]

    answers = inquirer.prompt(questions)

    api = TaigaAPI(
        host=answers['host']
    )

    api.auth(
        username=answers['user'],
        password=answers['password']
    )

    # print(projectsList)
    findproject = [
        inquirer.Text('project', message="taiga project" ),
    ]

    findprojectAnswers = inquirer.prompt(findproject)
    prjslug = findprojectAnswers['project']
    

    project = api.projects.get_by_slug(prjslug)

    milestones = api.milestones.list(project__name=project)
    milestonesList = []
    for el in milestones:
        milestonesList.append(el.name)

    selectsprint = [
        inquirer.List('sprint', message="Select your sprint", choices=milestonesList ),
    ]
    selectsprintAnswer = inquirer.prompt(selectsprint)
    sprint = selectsprintAnswer['sprint']

    tasks = api.tasks.list()
    sprint = api.milestones.list(project=project.id).filter(name=sprint)
    stories = api.user_stories.list(project__name=project,milestone=sprint[0].id)


    sourceHtml = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath='')).get_template(
        'template.html').render(date=date.today().strftime('%d, %b %Y'),
                                    stories=stories,tasks=tasks)
    
    outputFilename = "test.pdf"
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convertHtmlToPdf()