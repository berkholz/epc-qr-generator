# create directory for .app folder and move app folder to it
mkdir -p dist/dmg/
mv dist/EPC-QR-Generator.app dist/dmg/

# create dmg image with app
create-dmg \
  --volname "EPC-QR-Generator" \
  --volicon "epc-qr-generator.logo.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "EPC-QR-Generator.app" 175 120 \
  --hide-extension "EPC-QR-Generator.app" \
  --app-drop-link 425 120 \
  "dist/EPC-QR-Generator.dmg" \
  "dist/dmg/"
