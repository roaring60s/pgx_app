
import sys

path1 = sys.argv[1]
path2 = sys.argv[2]
path_out = sys.argv[3]

s = "\t"
sb = ""
sp = ","


def fnc_sample_from_asa(file1, file2, out):
	with open(file1, "r")as p1:
		counter = 0
		for ln1 in p1:
			counter = counter + 1
			ls1 = ln1.strip().split(s)
			mgrc_id1 = ls1[13]  # sample mgrc id in biodata file
			asa_name = ls1[16].split("_")[1]  # asa file name in biodata file
			pgx_id1 = ls1[2]  # sample pgx id in biodata file
			path5 = out + pgx_id1
			outfile = open(path5, "w+")
			print(counter, pgx_id1, asa_name, mgrc_id1, file2, sep=s)

			if asa_name in file2:
				with open(file2, "r")as p2:
					for ln2 in p2:
						ls2 = ln2.strip().split(s)
						mgrc_id2 = ls2[1]  # sample mgrc id in 7C_ASA file

						if mgrc_id1 == mgrc_id2:
							# noinspection PyTypeChecker
							print(s.join(ls2), sep=s, file=outfile)

	outfile.close()


fnc_sample_from_asa(path1, path2, path_out)
