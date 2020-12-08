from spellchecker import SpellChecker

spell = SpellChecker()

def similar(word):
    result = list(spell.candidates(word))
    result.append(spell.correction(word))
    return result
