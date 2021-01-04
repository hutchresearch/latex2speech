# coding: utf-8
import subprocess
import codecs

f = codecs.open("story.txt", encoding='utf-8')

cnt = 0
file_names = ''

for line in f:
    rendered = ''
    line = line.replace('"', '\\"')
    command = 'aws polly synthesize-speech --text-type ssml --output-format "mp3" --voice-id "Salli" --text "{0}" {1}'

    if '\r\n' == line:
        #A pause after a paragraph
        rendered = '<speak><break time= "2s"/></speak>'
    else:
        #A pause after a sentence
        rendered = '<speak><amazon:effect name=\\"drc\\">' + line.strip() + '<break time=\\"1s\\"/></amazon:effect></speak>'
    
    file_name = ' polly_out{0}.mp3'.format(u''.join(str(cnt)).encode('utf-8'))
    cnt += 1
    command = command.format(rendered.encode('utf-8'), file_name)
    file_names += file_name
    print(command)
    subprocess.call(command, shell=True)

print(file_names)
execute_command = 'cat ' + file_names + '>result.mp3'
subprocess.call(execute_command, shell=True)

execute_command = 'rm ' + file_names
print('Removing temporary files: ' + execute_command)
subprocess.call(execute_command, shell=True)