#!/bin/bash

# Self-Signed Certificate Setup (for testing/development)
# This creates self-signed certificates that work immediately
# Browser will show warning, but API calls will work fine

set -euo pipefail

DOMAIN1="dina.theokaitou.my.id"
DOMAIN2="ratu.theokaitou.my.id"
CERT_DIR="./nginx/certs"
DHPARAM_FILE="./nginx/dhparam.pem"
DAYS=365  # Certificate validity (1 year)

echo "🔐 Self-Signed Certificate Setup"
echo "=================================="
echo "Domains: $DOMAIN1, $DOMAIN2"
echo "Certificate directory: $CERT_DIR"
echo "Validity: $DAYS days"
echo ""

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

# Step 3: Generate self-signed certificate for domain 1
echo ""
echo "🚀 Generating self-signed certificate for $DOMAIN1..."
openssl req -x509 -newkey rsa:2048 -keyout "$CERT_DIR/$DOMAIN1/privkey.pem" -out "$CERT_DIR/$DOMAIN1/fullchain.pem" -days $DAYS -nodes \
    -subj "/CN=$DOMAIN1/O=TixGo/C=ID"

echo "✅ Certificate created for $DOMAIN1"
ls -lah "$CERT_DIR/$DOMAIN1/"

# Step 4: Generate self-signed certificate for domain 2
echo ""
echo "🚀 Generating self-signed certificate for $DOMAIN2..."
openssl req -x509 -newkey rsa:2048 -keyout "$CERT_DIR/$DOMAIN2/privkey.pem" -out "$CERT_DIR/$DOMAIN2/fullchain.pem" -days $DAYS -nodes \
    -subj "/CN=$DOMAIN2/O=TixGo/C=ID"

echo "✅ Certificate created for $DOMAIN2"
ls -lah "$CERT_DIR/$DOMAIN2/"

# Step 5: Start services
echo ""
echo "🚀 Starting services with HTTPS..."
docker compose -f docker-compose.prod.yml up -d

# Step 6: Test certificates
echo ""
echo "🧪 Testing HTTPS endpoints (ignore certificate warnings)..."
sleep 5

echo ""
echo "Testing $DOMAIN1 (ignore cert warning)..."
curl -k -s https://$DOMAIN1/health 2>/dev/null | jq . || echo "Connection failed (may be normal if still starting)"

echo ""
echo "Testing $DOMAIN2 (ignore cert warning)..."
curl -k -s https://$DOMAIN2/health 2>/dev/null | jq . || echo "Connection failed (may be normal if still starting)"

echo ""
echo "=========================================="
echo "✨ Self-Signed Setup Complete!"
echo ""
echo "Your services are now running with HTTPS:"
echo "  - https://$DOMAIN1"
echo "  - https://$DOMAIN2"
echo ""
echo "⚠️  Browser Warning:"
echo "  Browser will show certificate warning - this is normal"
echo "  Click 'Advanced' → 'Proceed anyway' or add exception"
echo ""
echo "🧪 To test API calls:"
echo "  curl -k https://$DOMAIN1/health"
echo "  curl -k https://$DOMAIN2/health"
echo ""
echo "📌 Certificate Details:"
openssl x509 -in "$CERT_DIR/$DOMAIN1/fullchain.pem" -text -noout | grep -A2 "Subject:\|Validity\|Public Key"
echo ""
echo "=========================================="
