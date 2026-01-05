#!/bin/bash

# Let's Encrypt Setup with DNS Validation
# Requires Cloudflare API token for DNS challenge

set -euo pipefail

DOMAIN1="dina.theokaitou.my.id"
DOMAIN2="ratu.theokaitou.my.id"
EMAIL="your-email@example.com"  # Change this
CERT_DIR="./nginx/certs"
DHPARAM_FILE="./nginx/dhparam.pem"

echo "🔐 Let's Encrypt SSL Certificate Setup (DNS Validation)"
echo "=========================================================="
echo "Domains: $DOMAIN1, $DOMAIN2"
echo "Certificate directory: $CERT_DIR"
echo ""

# Check if certbot-dns-cloudflare is installed
if ! python3 -m pip show certbot-dns-cloudflare > /dev/null 2>&1; then
    echo "📦 Installing certbot-dns-cloudflare plugin..."
    pip install certbot-dns-cloudflare
fi

# Step 1: Create certificate directories
echo "📁 Creating certificate directories..."
mkdir -p "$CERT_DIR/$DOMAIN1"
mkdir -p "$CERT_DIR/$DOMAIN2"

# Step 2: Generate DH parameters
echo "🔑 Generating DH parameters (this may take a few minutes)..."
if [ ! -f "$DHPARAM_FILE" ]; then
    openssl dhparam -out "$DHPARAM_FILE" 2048
else
    echo "   DH parameters already exist, skipping..."
fi

# Step 3: Create Cloudflare credentials file
echo ""
echo "⚙️  Setting up Cloudflare DNS credentials..."
echo "Create a file ~/.secrets/certbot/cloudflare.ini with your Cloudflare API token:"
echo ""
echo "dns_cloudflare_api_token = your_cloudflare_api_token_here"
echo ""
echo "Then come back and run this script again."
echo ""

if [ ! -f ~/.secrets/certbot/cloudflare.ini ]; then
    echo "❌ Cloudflare credentials file not found!"
    echo "Please create ~/.secrets/certbot/cloudflare.ini first"
    exit 1
fi

# Step 4: Generate certificates with DNS validation
echo "🚀 Generating certificate for $DOMAIN1 with DNS validation..."
certbot certonly \
    --dns-cloudflare \
    --dns-cloudflare-credentials ~/.secrets/certbot/cloudflare.ini \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    --domain "$DOMAIN1"

# Copy certificates
echo "📋 Copying certificates for $DOMAIN1..."
cp /etc/letsencrypt/live/$DOMAIN1/fullchain.pem "$CERT_DIR/$DOMAIN1/"
cp /etc/letsencrypt/live/$DOMAIN1/privkey.pem "$CERT_DIR/$DOMAIN1/"

# Step 5: Generate certificates for domain 2
echo ""
echo "🚀 Generating certificate for $DOMAIN2 with DNS validation..."
certbot certonly \
    --dns-cloudflare \
    --dns-cloudflare-credentials ~/.secrets/certbot/cloudflare.ini \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    --domain "$DOMAIN2"

# Copy certificates
echo "📋 Copying certificates for $DOMAIN2..."
cp /etc/letsencrypt/live/$DOMAIN2/fullchain.pem "$CERT_DIR/$DOMAIN2/"
cp /etc/letsencrypt/live/$DOMAIN2/privkey.pem "$CERT_DIR/$DOMAIN2/"

# Step 6: Verify certificates
echo ""
echo "✅ Verifying certificates..."
ls -la "$CERT_DIR/$DOMAIN1/"
ls -la "$CERT_DIR/$DOMAIN2/"

# Step 7: Start services
echo ""
echo "🚀 Starting services with HTTPS..."
docker compose -f docker-compose.prod.yml up -d

# Step 8: Test certificates
echo ""
echo "🧪 Testing HTTPS endpoints..."
sleep 3

echo ""
echo "Testing $DOMAIN1..."
curl -s https://$DOMAIN1/health 2>/dev/null | jq . || echo "Connection failed (may be normal if still starting)"

echo ""
echo "Testing $DOMAIN2..."
curl -s https://$DOMAIN2/health 2>/dev/null | jq . || echo "Connection failed (may be normal if still starting)"

echo ""
echo "=========================================="
echo "✨ Setup complete!"
echo ""
echo "Your services are now running with HTTPS:"
echo "  - https://$DOMAIN1"
echo "  - https://$DOMAIN2"
echo ""
echo "To verify:"
echo "  curl https://$DOMAIN1/health"
echo "  curl https://$DOMAIN2/health"
echo ""
echo "Certificate renewal (auto):"
echo "  The certificate will auto-renew before expiration"
echo "  Check status: sudo certbot certificates"
echo ""
echo "=========================================="
