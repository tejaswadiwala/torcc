class Product:
    class ClassicTee:
        def __init__(self): 
            self.title = ': Unisex Graphic T-shirt | Graphic Tees'
            self.body_html = "<p>TORCC studio brings you some quirky graphic tees. </p>\n<ul>\n<li>100% cotton</li>\n<li>Wash cold; dry low</li>\n<li>Imported</li>\n<li>Listed in men's/unisex sizes</li>\n</ul>"
            self.product_type = 'T-shirt'
            self.price = 21.99
            self.template_suffix = 'template-full-width-2'

    class OversizedTshirt:
        def __init__(self): 
            self.title = ': Oversized Graphic Tees'
            self.body_html = "<ul>\n<li>Made with 90% buttery soft cotton and&nbsp;10% breathable polyester</li>\n<li>Oversized fit for a relaxed and stylish look</li>\n<li>Bold durable graphic designs print stays the same wash after wash</li>\n<li>Ideal for lounging at home or running errands</li>\n<li>Ultimate combination of comfort and style</li>\n<li>Made to order in Canada<br></li>\n</ul>"
            self.product_type = 'Oversized T-shirt'
            self.price = 34.99
            self.template_suffix = 'template-full-width-2'