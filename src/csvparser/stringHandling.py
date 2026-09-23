class StringHandler():
    
    def _stringify_entries(self, entries: list) -> str:
            entries = str(entries).replace("'", '"')
            entries_str = ""
            for pc, cc, nc in zip(entries, entries[1:], entries[2:]):
                #print(f"pc: {pc}, cc: {cc}, nc: {nc}")
                if cc == '"' and pc not in [" ", "[", "{"] and nc not in [" ", ":", ",", "]", "}"] : # hvis en karakter følger og efterfølges af ikke-mellemrum eller særlige tegn, ændrer karakteren (antag at tegnet er inden i tekst)
                    entries_str += "'"
                
                else:
                    entries_str += cc

            entries_str = "["+entries_str+"]"
            return entries_str

    def _clean_string_as_csv(self, string: str, seperator):
            # must not end with a seperator
            while string.endswith(seperator) and isinstance(string, str) and len(string) > 1:
                string = string[0:-1]
            return string