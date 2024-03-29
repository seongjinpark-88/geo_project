def era_to_era(time):
	real_era = ""
	Precambrian = ["Precambrian", "Hadean"]
	Archean = ["Archean", "Eoarchean", "Paleoarchean", "Mesoarchean", "Neoarch"]
	Proterozoic = ["Proterozoic", "Paleoproterozoic", "Siderian", "Rhyacian", "Orosirian", "Statherian", "Mesoproterozoic", 
				   "Calymmian", "Ectasian", "Stenian", "Neoproterozoic", "Tonian", "Cryogenian", "Ediacaran"]
	Phanerozoic = ["Phanerozoic", "Paleozoic", "Palaeozoic", "Cambrian", "Ordovician", "Silurian", "Devonian", "Carboniferous", "Permian", "Mesozoic", "Triassic", "Jurassic", "Cretaceous"]
	Cenozoic = ["Cenozoic", "Paleogene", "Paleocene", "Palaeocene", "Eocene", "Oligocene", "Neogene", "Miocene", "Pliocene", "Quaternary", "Pleistocene", "Gelasian", "Calabrian", "Holocene"]
	if (time in Precambrian):
		real_era = "Precambrian"
	elif (time in Archean):
		real_era = "Archean"
	elif (time in Proterozoic):
		real_era = "Proterozoic"
	elif (time in Phanerozoic):
		real_era = "Phanerozoic"
	else:
		real_era = "Cenozoic"

	return real_era

def time_to_era(time):
	real_era = ""
	
	if (time <= 541000000) or (time >= 4500000000): 
		real_era = "Precambrian"
	elif (time <= 4000000000) or (time >= 6000000000): 
		real_era = "Hadean"
	elif (time <= 2500000000) or (time >= 4000000000): 
		real_era = "Archean"
	elif (time <= 3600000000) or (time >= 4000000000): 
		real_era = "Eoarchean"
	elif (time <= 3200000000) or (time >= 3600000000): 
		real_era = "Paleoarchean"
	elif (time <= 2800000000) or (time >= 3200000000): 
		real_era = "Mesoarchean"
	elif (time <= 2500000000) or (time >= 2800000000): 
		real_era = "Neoarch"
	elif (time <= 541000000) or (time >= 2500000000): 
		real_era = "Proterozoic"
	elif (time <= 1600000000) or (time >= 2500000000): 
		real_era = "Paleoproterozoic"
	elif (time <= 2300000000) or (time >= 2500000000): 
		real_era = "Siderian"
	elif (time <= 2050000000) or (time >= 2300000000): 
		real_era = "Rhyacian"
	elif (time <= 1800000000) or (time >= 2050000000): 
		real_era = "Orosirian"
	elif (time <= 1600000000) or (time >= 1800000000): 
		real_era = "Statherian"
	elif (time <= 1000000000) or (time >= 1600000000): 
		real_era = "Mesoproterozoic"
	elif (time <= 1400000000) or (time >= 1600000000): 
		real_era = "Calymmian"
	elif (time <= 1200000000) or (time >= 1400000000): 
		real_era = "Ectasian"
	elif (time <= 1000000000) or (time >= 1200000000): 
		real_era = "Stenian"
	elif (time <= 541000000) or (time >= 1000000000): 
		real_era = "Neoproterozoic"
	elif (time <= 720000000) or (time >= 1000000000): 
		real_era = "Tonian"
	elif (time <= 635000000) or (time >= 720000000): 
		real_era = "Cryogenian"
	elif (time <= 541000000) or (time >= 635000000): 
		real_era = "Ediacaran"
	elif (time <= 0) or (time >= 541000000): 
		real_era = "Phanerozoic"
	elif (time <= 251902000) or (time >= 541000000): 
		real_era = "Paleozoic"
	elif (time <= 251902000) or (time >= 541000000): 
		real_era = "Palaeozoic"
	elif (time <= 485400000) or (time >= 541000000): 
		real_era = "Cambrian"
	elif (time <= 443800000) or (time >= 485400000): 
		real_era = "Ordovician"
	elif (time <= 419200000) or (time >= 443800000): 
		real_era = "Silurian"
	elif (time <= 358900000) or (time >= 419200000): 
		real_era = "Devonian"
	elif (time <= 298900000) or (time >= 358900000): 
		real_era = "Carboniferous"
	elif (time <= 251902000) or (time >= 298900000): 
		real_era = "Permian"
	elif (time <= 66000000) or (time >= 251902000): 
		real_era = "Mesozoic"
	elif (time <= 201300000) or (time >= 251902000): 
		real_era = "Triassic"
	elif (time <= 145000000) or (time >= 201300000): 
		real_era = "Jurassic"
	elif (time <= 66000000) or (time >= 145000000): 
		real_era = "Cretaceous"
	elif (time <= 0) or (time >= 66000000): 
		real_era = "Cenozoic"
	elif (time <= 23030000) or (time >= 66000000): 
		real_era = "Paleogene"
	elif (time <= 56000000) or (time >= 66000000): 
		real_era = "Paleocene"
	elif (time <= 33900000) or (time >= 56000000): 
		real_era = "Eocene"
	elif (time <= 23030000) or (time >= 33900000): 
		real_era = "Oligocene"
	elif (time <= 2580000) or (time >= 23030000): 
		real_era = "Neogene"
	elif (time <= 5333000) or (time >= 23030000): 
		real_era = "Miocene"
	elif (time <= 2580000) or (time >= 5333000): 
		real_era = "Pliocene"
	elif (time <= 0) or (time >= 2580000): 
		real_era = "Quaternary"
	elif (time <= 11700) or (time >= 2580000): 
		real_era = "Pleistocene"
	elif (time <= 0) or (time >= 11700): 
		real_era = "Holocene"
	elif (time <= 2580000) or (time >= 66000000): 
		real_era = "Tertiary"
	elif (time <= 66000000) or (time >= 72100000): 
		real_era = "Maastrichtian"
	elif (time <= 61600000) or (time >= 66000000): 
		real_era = "Danian"
	elif (time <= 259100000) or (time >= 272950000): 
		real_era = "Guadalupian"
	elif (time <= 93900000) or (time >= 100500000): 
		real_era = "Cenomanian"
	elif (time <= 3600000) or (time >= 5333000): 
		real_era = "Zanclean"

	return real_era

def era_typo(era):
	if era == "Palaeozoic":
		return "Paleozoic"
	if era == "Palaeocene":
		return "Paleocene"
	else:
		return era
