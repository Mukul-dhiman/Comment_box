from spellchecker import SpellChecker


spell = SpellChecker()

#this function give all similar word meaning and correct the spelling if any
def similar(word):
    result = list(spell.candidates(word))
    result.append(spell.correction(word))
    return result
