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
    
    class ToteBags:
        def __init__(self): 
            self.title = ': Tote Bag'
            self.body_html = "<ul><li>Made with 100% soft and breathable cotton material</li><li>Spacious interior to carry all your essentials with ease</li><li>Stylish and versatile design for everyday use</li><li>Reinforced handles for comfortable and secure carrying</li><li>Features a bold graphic print that adds a touch of personality</li><li>Perfect for shopping, traveling, or daily errands</li><li>Eco-friendly choice to reduce single-use plastic bags</li><li>Easy to clean and maintain for long-lasting use</li><li>Express your unique sense of fashion with a TORCC tote bag made from 100% cotton.</li></ul>"
            self.product_type = 'Tote Bag'
            self.price = 24.99
            self.template_suffix = 'template-full-width-2'
    
    class ToteTshirtCoordSet:
        def __init__(self):
            self.title = ': Co-ord Set'
            self.body_html = "<p>Introducing our Tote T-shirt Co-ord Set - a match made in style heaven!</p><ul><li>🌟 Perfectly Coordinated: Our Co-ord Set includes a matching design t-shirt and tote bag for a cohesive and fashionable look.</li><li>🎨 Eye-Catching Design: Both the t-shirt and tote bag feature a captivating design that combines colors, patterns, or graphics.</li><li>👕 Comfortable T-Shirt: The high-quality t-shirt offers a comfortable fit, perfect for everyday wear and adding a touch of flair.</li><li>👜 Versatile Tote Bag: The stylish tote bag is not only a fashion accessory but also a practical companion with ample space and sturdy handles.</li><li>💃 Effortless Style: Achieve a coordinated look effortlessly without the hassle of searching for matching pieces.</li><li>🎁 Perfect Gift: The Co-ord Set makes a unique and thoughtful gift, showcasing impeccable taste.</li></ul><p>Elevate your style game with our Co-ord Set - the perfect combination for those who crave fashion-forward looks with ease. Get ready to turn heads and make a statement!</p>"
            self.product_type = 'Co-ord Set'
            self.price = 29.99
            self.template_suffix = 'template-full-width-2'