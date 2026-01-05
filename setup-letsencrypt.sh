#!/bin/bash

# Let's Encrypt Setup Script for TixGo Microservices
# This script generates SSL certificates using Let's Encrypt for:
# - dina.theokaitou.my.id (Identity Service)
# - ratu.theokaitou.my.id (Attendance Service)

set -euo pipefail

DOMAIN1="dina.theokaitou.my.id"
DOMAIN2="ratu.theokaitou.my.id"
EMAIL="your-email@example.com"  # Change this to your email
CERT_DIR="./nginx/certs"
DHPARAM_FILE="./nginx/dhparam.pem"

echo "🔐 Let's Encrypt SSL Certificate Setup"
echo "=========================================="
echo "Domains: $DOMAIN1, $DOMAIN2"
echo "Certificate directory: $CERT_DIR"
echo ""

# Step 1: Create certificate directories
echo "📁 Creating certificate directories..."
mkdir -p "$CERT_DIR/$DOMAIN1"
mkdir -p "$CERT_DIR/$DOMAIN2"

# Step 2: Generate DH parameters (for stronger SSL)
echo "🔑 Generating DH parameters (this may take a few minutes)..."
if [ ! -f "$DHPARAM_FILE" ]; then
    openssl dhparam -out "$DHPARAM_FILE" 2048
else
    echo "   DH parameters already exist, skipping..."
fi

# Step 3: Stop nginx temporarily
echo "⏹️  Stopping nginx temporarily..."
docker compose -f docker-compose.prod.yml down nginx || true
sleep 2

# Step 4: Generate certificates for domain 1
echo ""
echo "🚀 Generating certificate for $DOMAIN1..."
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    --domain "$DOMAIN1"

# Copy certificates to nginx cert directory
echo "📋 Copying certificates for $DOMAIN1..."
sudo cp /etc/letsencrypt/live/$DOMAIN1/fullchain.pem "$CERT_DIR/$DOMAIN1/"
sudo cp /etc/letsencrypt/live/$DOMAIN1/privkey.pem "$CERT_DIR/$DOMAIN1/"
sudo chown -R $USER:$USER "$CERT_DIR/$DOMAIN1"

# Step 5: Generate certificates for domain 2
echo ""
echo "🚀 Generating certificate for $DOMAIN2..."
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    --domain "$DOMAIN2"

# Copy certificates to nginx cert directory
echo "📋 Copying certificates for $DOMAIN2..."
sudo cp /etc/letsencrypt/live/$DOMAIN2/fullchain.pem "$CERT_DIR/$DOMAIN2/"
sudo cp /etc/letsencrypt/live/$DOMAIN2/privkey.pem "$CERT_DIR/$DOMAIN2/"
sudo chown -R $USER:$USER "$CERT_DIR/$DOMAIN2"

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
curl -s https://$DOMAIN1/health | jq . || echo "Failed to connect to $DOMAIN1"

echo ""
echo "Testing $DOMAIN2..."
curl -s https://$DOMAIN2/health | jq . || echo "Failed to connect to $DOMAIN2"

echo ""
echo "=========================================="
echo "✨ Setup complete!"
echo ""
echo "Your services are now running with HTTPS:"
echo "  - https://$DOMAIN1"
echo "  - https://$DOMAIN2"
echo ""
echo "Certificate renewal:"
echo "  sudo certbot renew --dry-run  # Test renewal"
echo "  sudo certbot renew             # Auto-renew certificates"
echo ""
echo "View certificate details:"
echo "  sudo certbot certificates"
echo ""
echo "=========================================="
