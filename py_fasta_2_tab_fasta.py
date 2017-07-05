import pandas as pd

def py_fasta_2_tab_fasta(fasta_file, output_name):
    """
    written by peteskene@gmail.com
    
    takes in a standard fasta file e.g.
    >id_1
    sequence_1_a
	sequence_1_b
    >id_2
    sequence_2
    
    and converts to a tab delimited file and saves to output_name (no header)
    id_1    sequence_1_a + sequence_1_b
    id_2    sequence_2
    
    script will accept text wrapping in the input fasta file
    
    """
    #create empty dataframe to be filled by fasta file
    temp_df = pd.DataFrame(columns=['id', 'sequence'])
    
    #create empty list to hold each row as it is made
    temp_list = []
        
    with open(fasta_file) as myfastafile:
        for line in myfastafile:
            if line.startswith('>'):
                if len(temp_list)!=0: #this means finished reading the previous fasta entry, so need to add to temp_df
                    
                    #need to consider fasta file where there is text wrapping with sequence on multiple lines
                    if len(temp_list)>2:
                        temp_list = [temp_list[0], temp_list[1]+temp_list[2]]
                    
                    temp_df = pd.concat([temp_df, pd.DataFrame([temp_list], columns=['id', 'sequence'])])
                
                temp_list = [] #now reset the temp_list to empty to start this entry
                temp_list.append(line.replace('>', '').replace('\r\n', ''))
                
                
            else:
                temp_list.append(line.replace('\r\n', ''))
                
        
        #need to add the last row to temp_df
        #need to consider fasta file where there is text wrapping with sequence on multiple lines
        if len(temp_list)>2:
            temp_list = [temp_list[0], temp_list[1]+temp_list[2]]

        temp_df = pd.concat([temp_df, pd.DataFrame([temp_list], columns=['id', 'sequence'])])
        
        #save file
        temp_df.to_csv(output_name, sep='\t', header=False, index=False)
        
    return temp_df
