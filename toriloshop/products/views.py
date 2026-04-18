from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Torilo Shop - Welcome</title>
    
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Torilo Shop!</h1>
            <p>Welcome to Torilo Shop - your premier destination for quality products and exceptional service.</p>
            <p>We are committed to providing you with the best shopping experience online. 
            Discover our wide selection of products, competitive prices, and fast delivery.</p>
            <p><strong>Why choose Torilo Shop?</strong></p>
            <ul>
                <li>High-quality products</li>
                <li>Competitive pricing</li>
                <li>Fast and reliable shipping</li>
                <li>Excellent customer service</li>
                <li>Secure payment options</li>
            </ul>
            <div class="nav-links">
                <h3>Quick Navigation:</h3>
                <a href="/products/">View Products</a>
                <a href="/about/">About Us</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)


def product_list(request):

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Products - Torilo Shop</title>
    </head>
    <body>
        <h1>Our Products</h1>
        <p>Browse our selection of quality products:</p>
        
        <h2>Premium Wireless Headphones</h2>
        <p>High-quality audio with noise cancellation. Perfect for music lovers and professionals.</p>
        <p><strong>Price: $79.99</strong></p>
        
        <h2>Leather Laptop Bag</h2>
        <p>Durable and stylish bag designed for professionals. Fits 15-inch laptops.</p>
        <p><strong>Price: $49.99</strong></p>
        
        <h2>Smart Watch</h2>
        <p>Stay connected with fitness tracking and notifications. Battery lasts 7 days.</p>
        <p><strong>Price: $199.99</strong></p>
        
        <h2>USB-C Charging Cable</h2>
        <p>Fast charging cable compatible with all USB-C devices. 2-meter length.</p>
        <p><strong>Price: $12.99</strong></p>
        
        <hr>
        <p><a href="/">← Back to Home</a> | <a href="/about/">About Us →</a></p>
    </body>
    </html>
    """
    return HttpResponse(html_content)
    return HttpResponse(html_content)


def about(request):

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>About Us - Torilo Shop</title>
        
    </head>
    <body>
        <div class="container">
            <h1>About Torilo Shop</h1>
            
            <h2>Our Story</h2>
            <div class="about-section">
                <p>Torilo Shop was founded with a mission to provide customers with quality products 
                at affordable prices. We believe in offering exceptional service and building long-term 
                relationships with our customers.</p>
            </div>
            
            <h2>Our Mission</h2>
            <div class="about-section">
                <p>To deliver high-quality products and outstanding customer service that exceeds 
                expectations and builds trust with every customer interaction.</p>
            </div>
            
            <h2>Why We're Different</h2>
            <div class="about-section">
                <ul>
                    <li><strong>Quality Assurance:</strong> Every product is carefully selected and tested</li>
                    <li><strong>Customer First:</strong> Your satisfaction is our top priority</li>
                    <li><strong>Fast Delivery:</strong> Quick and reliable shipping to your doorstep</li>
                    <li><strong>Competitive Prices:</strong> Best value for your money</li>
                    <li><strong>Expert Support:</strong> Knowledgeable team ready to help</li>
                </ul>
            </div>
            
            <h2>Contact Information</h2>
            <div class="about-section">
                <p>Email: <strong>support@toriloshop.com</strong></p>
                <p>Phone: <strong>1-800-TORILO-1</strong></p>
                <p>Address: <strong>123 Shopping Street, Commerce City, CC 12345</strong></p>
            </div>
            
            <div class="back-link">
                <a href="/">← Back to Home</a> | 
                <a href="/products/">View Products →</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)


def page_not_found(request, exception=None):
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Page Not Found</title>
        
    </head>
    <body>
        <div class="container">
            <h1>404</h1>
            <h2>Page Not Found</h2>
            <div class="error-message">
                <p>Sorry! The page you're looking for doesn't exist or has been moved.</p>
            </div>
            <p>The requested URL was not found on this server.</p>
            <p>Let's get you back on track:</p>
            <p>
                <a href="/">← Home</a> | 
                <a href="/products/">Products</a> | 
                <a href="/about/">About Us</a>
            </p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, status=404)
