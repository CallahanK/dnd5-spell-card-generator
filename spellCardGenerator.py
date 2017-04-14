#!/usr/bin/env python3
# PHB_Spells_3.9.0.xml


def main():

    import argparse
    import xml.etree.ElementTree as ET
    tree = ET.parse('./PHB_Spells_3.9.0.xml')
    root = tree.getroot()

    htmlPageString = open('html_page.template', 'r').read()
    spellDivString = open('spell_div.template', 'r').read()
    from string import Template
    htmlPageTemplate = Template(htmlPageString)
    spellDivTemplate = Template(spellDivString)

    htmlOutput = open('output_test.html', 'w')

    # TODO set via args
    # filters
    classes = ["Ranger", "Wizard"]
    level = 3  # TODO add less then, also use 0 for cantrips 
    school = ['A', 'EN']  # abbrv
    ritual = True

    spellDivList = []

    for spell in root:

        classes = spell.find('classes').text
        if "Bard" in classes:

            mySpell = parseXMLtoSpell(spell)

            spellDivList.append(spellDivTemplate.safe_substitute(mySpell.__dict__))
            # mySpell.display()
            # out.write(template.safe_substitute(mySpell.__dict__))
            # mySpell.toHTML()
            # break

    print(len(spellDivList))
    htmlOutput.write(htmlPageTemplate.safe_substitute(content_all=" ".join(spellDivList)))


def parseXMLtoSpell(spell):
    name = spell.find('name').text
    level = spell.find('level').text
    school = spell.find('school').text
    ritual = spell.findtext('ritual', 'false')
    time = spell.find('time').text
    target = spell.find('range').text
    components = spell.find('components').text
    duration = spell.find('duration').text

    text = []
    for text_block in spell.findall('text'):
        if text_block.text is not None:
            text.append(text_block.text)

    mySpell = Spell(name, level, school, ritual,
                    time, target, components, duration, text)
    return mySpell


class Spell:

    schools = {
        'A': 'Abjuration',
        'C': 'Conjuration',
        'D': 'Divination',
        'EN': 'Enchantment',
        'EV': 'Evocation',
        'I': 'Illusion',
        'N': 'Necromancy',
        'T': 'Transmutation',
    }

    def __init__(
        self, name, level, school, ritual,
            time, target, components, duration, text):
        self.name = name
        self.level = level if (level != 0) else "Cantrip"
        self.school = self.schools[school]
        self.ritual = ritual == 'YES'
        self.time = time
        self.target = target
        self.components = components
        self.duration = duration
        self.text = text
        self.htmlText = '\n'.join('<p>{0}</p>'.format(t) for t in text)
        # '<p>{0}</p>'.format('\n'.join(text))
        # self.htmlText = "<br>".join(text)

    def display(self):
        print("Name: " + self.name)
        print("Level: " + self.level)
        print(self.school)
        if(self.ritual):
            print("Ritual")
        print("Casting Time: " + self.time)
        print("Target: " + self.target)
        print("Components: " + self.components)
        print("Duration: " + self.duration)
        for block in self.text:
            print(block)
        print()

    def toHTML(self):
        pass


if __name__ == "__main__":
    main()
