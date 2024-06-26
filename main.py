'''Changing one line of G84 with tapping to many incremental lines with final Z value'''
def drop_files(file_name:str= 'Gwint', copy_suffix:str= '_x_mod',peek_inc:float= 1.25):
    """ This function open nc file and copy its content to new file with given suffix.
    If function find line with G84 code (which mean tapping),
    its split line with Z increment till orginal z_max value.
     """
    copy = file_name + copy_suffix
    with (open(file_name + '.nc', 'r',encoding='UTF-8') as org_file,
          open(copy + '.nc', 'w',encoding='UTF-8') as copy_file):
        new_list = []
        for line in org_file:
            if 'G84' in line:
                n, fun, fun1, r, z, f = line.strip().split(' ')
                copy_file.writelines('\n')
                copy_file.write(f'{n} (Podmieniono wartosc {z} na ciag:) \n')

                z_max = abs(float(z[1:]))
                current_z = 0
                while current_z <= z_max:
                    if current_z >= z_max:
                        break

                    current_z += peek_inc
                    if current_z >= z_max:
                        current_z = z_max

                    new_line = [fun, fun1, r, 'Z-' + str(f'{current_z:.2f}'), f]
                    str_new_line = ' '.join(new_line)
                    copy_file.write(str_new_line)
                    copy_file.writelines('\n')
                    new_list.append(str_new_line)
                new_list.append('G80\n')
                copy_file.write('G80\n') #TYLKO JEZELI PO G80 JEST G00
                current_z = 0
            elif 'G80' in line:
                new_list.clear()
            elif len(new_list) > 0 and not 'G80' in line:
                copy_file.write(line)
                for value in new_list:
                    copy_file.write(value + '\n')

            else:
                copy_file.write(line)

drop_files(file_name='plytka', copy_suffix='_MOD', peek_inc=1.75)
