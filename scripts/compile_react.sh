rm -r client/build
rm -r apps/main/static/
rm apps/main/templates/main/index.html
cd client/
npm run build
mv -f build/index.html ../apps/main/templates/main/
mv -f build/* build/static/
mv -f build/static/* build/static/
cp -r build/static/ ../apps/main/
cd ..
echo "Compiled succesfully"
