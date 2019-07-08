import lxml.etree as ET
import pdfkit
import os
import PySimpleGUI as sg
config = pdfkit.configuration(wkhtmltopdf=os.path.expanduser(r'~\Documents\wkhtmltopdf.exe'))  # file path of wkhtmltopdf.exe file
options = {
    'encoding': "UTF-8",    # encoding type
}

layout = [[sg.Text('   ')],
          [sg.Text('Folder'), sg.InputText(size=(50, 1)), sg.FolderBrowse()], [sg.Text('   ')],
          [sg.Submit(button_color=('black', 'light blue')), sg.Text(' '),
           sg.Quit(tooltip='Quit to Exit')]]

window = sg.Window('XML Auto PDF generator').Layout(layout)

'''
/////////////////
    Main loop
/////////////////
'''

def event_gui():

    event, (Folder,) = window.Read()

    while True or event is not None or event != 'Quit':

        if event is None or event == 'Quit':
            window.Close()
            break

        elif Folder == '':
            sg.PopupError('Oops, you forgot to input a Folder')

        else:
            entries = os.listdir(os.path.expanduser(Folder))

            xml_list = [i for i in entries if '.xml' in i]

            html_name = [i.replace('.xml', '.html') for i in xml_list]

            pdf_name = [i.replace('.xml', '.pdf') for i in xml_list]

            for num, xml_target in enumerate(xml_list):
                try:

                    xsltfile = ET.XSLT(ET.parse(os.path.expanduser(r'~\Documents\test\AQSVMobile_SS1.xsl')))

                    xmlfile = ET.parse(Folder + '/' + xml_target)

                    xsltfile(xmlfile).write_output(os.path.expanduser(Folder + '/' + html_name[num]))

                    paths = os.path.expanduser(Folder + '/' + pdf_name[num])

                    with open(os.path.expanduser(Folder + '/' + html_name[num])) as f:
                        pdfkit.from_file(f, paths, configuration=config)

                    os.remove(os.path.expanduser(Folder + '/' + html_name[num]))

                except Exception as a:
                    sg.Popup(a, '-------------------', 'Show this to Chris')
                    break
            event_gui()
            break
        event_gui()
        break

    window.Close()

event_gui()
