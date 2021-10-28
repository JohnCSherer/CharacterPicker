import random

def getNext(string, delim):
	sub = ""
	nextLineIndex = string.find(delim)
	if nextLineIndex == -1:
		sub = string
	else:
		sub = string[0:nextLineIndex]
	return sub

def removeNext(string, delim):
	nextLineIndex = string.find(delim)
	if nextLineIndex == -1:
		string = ""
	else:
		string = string[nextLineIndex+1:]
	return string

def existsCat(cat, rowNames):
	return cat in rowNames[1:] or cat.capitalize() in rowNames[1:] or cat.casefold() in rowNames[1:]

def characterIn(name, category):
	return name in category or name.capitalize() in category or name.casefold() in category

def characterIndex(name, category):
	if name in category:
		return category.index(name)
	if name.capitalize() in category:
		return category.index(name.capitalize())
	elif name.casefold() in category:
		return category.index(name.casefold())
	print("ERROR: CharacterIndex failed to find char in array")

def indexCat(cat, rowNames):
	if cat in rowNames[1:]:
		return rowNames.index(cat)
	if cat.capitalize() in rowNames[1:]:
		return rowNames.index(cat.capitalize())
	elif cat.casefold() in rowNames[1:]:
		return rowNames.index(cat.casefold())
	else:
		print("Error, could not find the category \"" + cat + "\"")
		return None

def trim(string):
	while string != "" and string[0:1] == " ":
		string = string[1:]
	return string

def trimEnd(string):
	while string != "" and string[-1:] == " ":
		string = string[:-1]
	return string

def save(rowNames, row):
	finalString = ""
	for i in range(0, len(rowNames)):
		finalString = finalString + rowNames[i] + "$"
		for j in range(0, len(row[i])):
			finalString = finalString + row[i][j] + "$"
		finalString = finalString[:-1] + "@"
	finalString = finalString[:-1]
	file = open("characters.txt", "w")
	file.write(finalString)

def waitForAnswer(query):
	inp = input(query + "\n>>>").casefold()
	while True:
		if inp in ["yes", "ye", "yeye", "y", "yee", "yeah", "yes please", "yes, please", "yep", "sure"]:
			return True
		elif inp in ["no", "nope", "nah", "no thanks", "no thank you", "n", "nee"]:
			return False
		inp = input("Did not recognize input. Please indicate yes or no\n>>>").casefold()

def main():
	file = open("characters.txt", "r")
	f = file.read()
	row = []
	rowNames = ["General"]
	sub = getNext(f, "@")
	f = removeNext(f, "@")
	sub = removeNext(sub,"$")
	nextRow = []
	while sub != "":
		nextRow.append(getNext(sub,"$"))
		sub = removeNext(sub,"$")
	row.append(nextRow)
	while f != "":
		sub = getNext(f, "@")
		f = removeNext(f, "@")
		rowNames.append(getNext(sub,"$"))
		sub = removeNext(sub,"$")
		nextRow = []
		while sub != "":
			nextRow.append(getNext(sub,"$"))
			sub = removeNext(sub,"$")
		row.append(nextRow)


	print("""Welcome to Character Roller! Here are the basic commands\n
	add [name] = add a character to the general list\n
	roll = get a random character from the general list\n
	add [name] to [category] = add a character to the category and the general list\n
	roll [category] = get a random character from a specific category\n
	remove [name] from [category] = remove the character from the category\n
	remove [name] from all = remove the character from every category and the general list\n
	remove [category] = remove the entire category\n
	view [category] = print out all the members of a category\n
	view categories = print out the names of all the categories\n
	view = print out all members of all categories\n
	save = saves all changes to the file\n
	help = see this information again\n
	exit = quit the program""")
	loop(rowNames, row)

def loop(rowNames, row):
	while True:
		i = input("\n>>>")
		i = trimEnd(trim(i))
		if(i == "exit"):
			if waitForAnswer("Would you like to save?"):
				save(rowNames, row)
			exit()
		elif(i == "help"):
			print("""Welcome to Character Roller! Here are the basic commands\n
	add [name] = add a character to the general list\n
	roll = get a random character from the general list\n
	add [name] to [category] = add a character to the category and the general list\n
	roll [category] = get a random character from a specific category\n
	remove [name] from [category] = remove the character from the category\n
	remove [name] from all = remove the character from every category and the general list\n
	remove [category] = remove the entire category\n
	view [category] = print out all the members of a category\n
	view categories = print out the names of all the categories\n
	view = print out all members of all categories\n
	save = saves all changes to the file\n
	help = see this information again\n
	exit = quit the program""")
		elif(i[:4] == "view"):
			cat = trim(i[4:])
			if cat == "":
				for i in range(len(rowNames)):
					print("\n-= " + rowNames[i] + " =-")
					for j in range(len(row[i])):
						print(row[i][j])
			elif cat == "categories":
				for i in range(1,len(rowNames)):
					print("-=" + rowNames[i] + "=-")
			elif existsCat(cat, rowNames):
				print("-= " + cat + " =-")
				for char in row[indexCat(cat, rowNames)]:
					print(char)
			else:
				print("Error, did not recognize command past the word \"view\"")
		elif(i[:4].casefold() == "roll"):
			i = i[4:]
			cat = trimEnd(trim(i))
			if cat == "":
				print("Random character: " + random.choice(row[0]))
			elif existsCat(cat, rowNames):
				print("Random character from " + cat + ": " + random.choice(row[indexCat(cat,rowNames)]))
			else:
				print("Error, could not find the category \"" + cat + "\"")
		elif(i[:3].casefold() == "add"):
			i = i[3:]
			i = trim(i)
			toIndex = i.find(" to ")
			if toIndex == -1:
				if i == "":
					print("Error, incomplete command")
				elif characterIn(i, row[0]):
					print(i + " is already in the general character list")
				else:
					row[0].append(i)
					print("Added " + i + " to the general character list")
			else:
				charName = trimEnd(trim(i[:toIndex]))
				cat = trimEnd(trim(i[toIndex+4:]))
				if charName == "":
					print("Error, incomplete command")
				elif not existsCat(cat, rowNames):
					if waitForAnswer("Could not find the category \"" + cat + "\", create it?"):
						if not characterIn(charName, row[0]):
							row.append([charName])
							rowNames.append(cat)
							row[0].append(charName)
							print("Added " + charName + " to " + cat + " and the general character list")
						else:
							row.append([charName])
							rowNames.append(cat)
							print("Added " + charName + " to the category " + cat)
					else:
						print("Aborted character/category creation")
				elif not characterIn(charName, row[indexCat(cat, rowNames)]):
					if not characterIn(charName, row[0]):
						row[0].append(charName)
						row[indexCat(cat, rowNames)].append(charName)
						print("Added " + charName + " to " + cat + " and the general character list")
					else:
						row[indexCat(cat, rowNames)].append(charName)
						print("Added " + charName + " to the category " + cat)
				else:
					print(charName + " is already in " + cat)
		elif(i[:4] == "save"):
			save(rowNames, row)
			print("Data saved successfully")
		elif(i[:6] == "remove"):
			i = trim(i[6:])
			fromIndex = i.find("from ")
			if fromIndex == -1:
				cat = i
				if existsCat(cat,rowNames):
					if waitForAnswer("Are you sure you want to delete the category \"" + cat + "\"?"):
						row[indexCat(cat, rowNames)].clear()
						rowNames.pop(indexCat(cat,rowNames))
						print("Category successfully removed")
					else:
						print("Aborting deletion")
				else:
					print("Error, could not find category \"" + cat + "\"")
			else:
				charName = trimEnd(trim(i[:fromIndex]))
				cat = trim(i[fromIndex+5:])
				if cat.casefold() == "all":
					if characterIn(charName, row[0]):
						if waitForAnswer("Are you sure you want to delete all instances of \"" + charName + "\"?"):
							for r in row:
								if characterIn(charName, r):
									r.pop(characterIndex(charName, r))
							print(charName + " successfully removed from all categories")
						else:
							print("Aborting deletion")
					else:
						print("Error, could not find character \"" + charName + "\" in the general list")
				elif existsCat(cat, rowNames):
					if characterIn(charName, row[indexCat(cat, rowNames)]):
						row[indexCat(cat, rowNames)].remove(charName)
						print("Successfully removed \"" + charName + "\" from category \"" + cat + "\"")
					else:
						print("Error, could not find character \"" + charName + "\" in category \"" + cat + "\"")
				else:
					print("Error, could not find category \"" + cat + "\"")
		else:
			print("Error, did not recognize command")

if __name__ == "__main__":
    main()