echo "Fake email server listening at 'localhost:1025'"
python -m smtpd -n -c DebuggingServer localhost:1025
