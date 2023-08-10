class Product:
    class ClassicTee:
        def __init__(self): 
            self.dir_name = 'classic_tees'

    class OversizedTshirt:
        def __init__(self): 
            self.dir_name = 'oversized_tees'
    
    class ToteBags:
        def __init__(self):
            self.dir_name = 'tote_bags'
    
    class Hoodies:
        class Front: 
            def __init__(self):
                self.dir_name = 'hoodies/front'
        class Back: 
            def __init__(self):
                self.dir_name = 'hoodies/back'