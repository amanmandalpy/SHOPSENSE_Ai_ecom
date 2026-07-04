import os

EMAIL_DIR = 'd:\\PYTHON_PROJECTS\\SHOPSENSE_Ai_ecommerce\\templates\\emails'
os.makedirs(EMAIL_DIR, exist_ok=True)

base_css = """
        body { font-family: 'Inter', Helvetica, Arial, sans-serif; background-color: #f3f4f6; color: #1f2937; margin: 0; padding: 0; }
        .wrapper { padding: 40px 20px; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; padding: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .logo { font-size: 24px; font-weight: 800; color: #3b82f6; margin-bottom: 30px; letter-spacing: -0.5px; }
        .btn { display: inline-block; padding: 14px 28px; background-color: #3b82f6; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px; text-align: center; }
        .footer { margin-top: 40px; font-size: 13px; color: #9ca3af; text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px; }
"""

templates = {
    'welcome.html': f"""<!DOCTYPE html><html><head><style>{base_css}</style></head><body><div class="wrapper"><div class="container">
        <div class="logo">ShopSense AI</div>
        <h2>Welcome to ShopSense AI!</h2>
        <p>Hi {{{{ user.first_name|default:"there" }}}},</p>
        <p>We are thrilled to welcome you to the future of smart shopping.</p>
        <a href="{{{{ site_url }}}}" class="btn">Start Exploring</a>
        <div class="footer">&copy; {{{{ current_year }}}} ShopSense AI. All rights reserved.</div>
    </div></div></body></html>""",
    
    'verify_email.html': f"""<!DOCTYPE html><html><head><style>{base_css}</style></head><body><div class="wrapper"><div class="container">
        <div class="logo">ShopSense AI</div>
        <h2>Verify your email address</h2>
        <p>Hi {{{{ name|default:"there" }}}},</p>
        <p>Please click the button below to verify your email address and activate your newsletter subscription.</p>
        <a href="{{{{ verify_url }}}}" class="btn">Verify Email</a>
        <div class="footer">&copy; {{{{ current_year }}}} ShopSense AI. All rights reserved.</div>
    </div></div></body></html>""",
    
    'reset_password.html': f"""<!DOCTYPE html><html><head><style>{base_css}</style></head><body><div class="wrapper"><div class="container">
        <div class="logo">ShopSense AI</div>
        <h2>Password Reset Request</h2>
        <p>Hi {{{{ user.first_name|default:"there" }}}},</p>
        <p>We received a request to reset your password. Click the button below to choose a new one:</p>
        <a href="{{{{ reset_url }}}}" class="btn">Reset Password</a>
        <p style="margin-top:20px; font-size:12px; color:#6b7280;">If you didn't request this, you can safely ignore this email.</p>
        <div class="footer">&copy; {{{{ current_year }}}} ShopSense AI.</div>
    </div></div></body></html>""",
    
    'price_alert.html': f"""<!DOCTYPE html><html><head><style>{base_css}</style></head><body><div class="wrapper"><div class="container">
        <div class="logo">ShopSense AI</div>
        <h2>Good news! A price dropped.</h2>
        <p>The price for <strong>{{{{ product.name }}}}</strong> has dropped to <strong>${{{{ current_price }}}}</strong> (Target: ${{{{ target_price }}}}).</p>
        <a href="{{{{ product_url }}}}" class="btn">View Deal</a>
        <div class="footer">You received this because you set a price alert. &copy; {{{{ current_year }}}} ShopSense AI.</div>
    </div></div></body></html>""",
    
    'newsletter.html': f"""<!DOCTYPE html><html><head><style>{base_css}</style></head><body><div class="wrapper"><div class="container">
        <div class="logo">ShopSense AI</div>
        <h2>{{{{ subject }}}}</h2>
        <div>{{{{ content|safe }}}}</div>
        <div class="footer">
            <p>You are receiving this because you subscribed to our newsletter.</p>
            <p><a href="{{{{ unsubscribe_url }}}}" style="color:#9ca3af; text-decoration:underline;">Unsubscribe</a></p>
            &copy; {{{{ current_year }}}} ShopSense AI.
        </div>
    </div></div></body></html>""",
    
    'contact_ack.html': f"""<!DOCTYPE html><html><head><style>{base_css}</style></head><body><div class="wrapper"><div class="container">
        <div class="logo">ShopSense AI</div>
        <h2>We received your message</h2>
        <p>Hi {{{{ name }}}},</p>
        <p>Thank you for reaching out to ShopSense Support. We have received your ticket regarding <strong>"{{{{ subject }}}}"</strong>.</p>
        <p>Our team will review it and get back to you shortly.</p>
        <div class="footer">&copy; {{{{ current_year }}}} ShopSense AI.</div>
    </div></div></body></html>""",
    
    'system_notification.html': f"""<!DOCTYPE html><html><head><style>{base_css}</style></head><body><div class="wrapper"><div class="container">
        <div class="logo">ShopSense AI</div>
        <h2>System Notification</h2>
        <p>{{{{ message|safe }}}}</p>
        <div class="footer">&copy; {{{{ current_year }}}} ShopSense AI.</div>
    </div></div></body></html>"""
}

for filename, content in templates.items():
    with open(os.path.join(EMAIL_DIR, filename), 'w') as f:
        f.write(content)
print("Email templates generated.")
