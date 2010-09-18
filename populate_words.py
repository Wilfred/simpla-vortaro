from vortaro.models import Word

"""Load up the dictionary with the values in a word list. Running
standalone scripts is a slight fiddle in Django, so run by:

$ python manage.py shell
In [1]: import populate_words

"""

word_list = open('/home/wilfred/html/vortaro/python/word_list.txt',
                 'r').readlines()

for word in word_list:
    w = Word(word=word.strip())
    w.save()
