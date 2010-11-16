"""Exploring morphology parsing weightings to ensure we only return
correct parses.


Format: (input, correct_parses_in_priority_order, incorrect_parses)

"""

('homarano', ['hom-ar-an-o', 'homa-ran-o'], ['ho-mar-an-o'])
('alies', [], ['al-ies'])
('hundomalfermilo', ['hundo-mal-ferm-il-o'], ['hundo-mal-fer-mil-o', 'hundo-mal-ferm-il-o', 'hun-do-mal-fer-mil-o', 'hun-do-mal-ferm-il-o', 'hun-dom-al-fer-mil-o', 'hun-dom-al-ferm-il-o', 'hun-dom-alf-er-mil-o'])
('persone', ['person-e', 'per-son-e'], ['pers-on-e'])
('altabligi', ['al-tabl-ig-i'], ['al-tab-ligi'])
('manĝilaro', ['manĝ-il-ar-o'], ['man-ĝi-lar-o'])
('renovigi', ['re-nov-ig-i'], ['ren-ov-ig-i'])
('ripozejo', ['ripoz-ej-o'], ['ri-poz-ej-o'])
('neniigi', ['neni-ig-i'], ['ne-ni-ig-i'])
('pintigi', ['pint-ig-i'], ['pin-tig-i'])
('surdomutulo'
('senlaborulo'
('ĉirkaŭrigardi'
('eksilentigi'


