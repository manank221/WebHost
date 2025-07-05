# Deploy Your Django Website to Render

## Prerequisites
- GitHub account
- Render account (free at https://render.com)

## Step 1: Push Your Code to GitHub

1. Initialize git (if not already done):
```bash
git init
git add .
git commit -m "Initial commit for deployment"
```

2. Create a new repository on GitHub and push:
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Render

1. Go to [https://render.com](https://render.com) and sign up/log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

### Build & Deploy Settings:
- **Name**: `your-website-name`
- **Environment**: `Python 3`
- **Build Command**: 
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```
- **Start Command**: 
```
gunicorn freelance_website.wsgi
```

### Environment Variables:
Add these in the Render dashboard:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

5. Click **"Create Web Service"**

## Step 3: Create Superuser

After deployment, create a superuser to access the admin:

1. Go to your Render dashboard
2. Click on your web service
3. Go to **"Shell"** tab
4. Run:
```bash
python manage.py createsuperuser
```

## Step 4: Access Your Website

- **Main Website**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`

## Step 5: Share with Your Team

Share the URLs with your team members. They can:
- View the website anytime
- Access the admin panel from anywhere
- No need to run localhost

## Troubleshooting

### If you get a 500 error:
1. Check the logs in Render dashboard
2. Make sure all environment variables are set
3. Verify your database migrations ran

### If static files don't load:
1. Make sure `collectstatic` ran during build
2. Check that `STATIC_ROOT` is set correctly
3. Verify WhiteNoise is in your middleware

### If admin doesn't work:
1. Make sure you created a superuser
2. Check that the database is properly migrated
3. Verify your secret key is set correctly

## Security Notes

- Never commit your `.env` file to git
- Use strong passwords for admin accounts
- Consider using environment variables for sensitive data
- Enable HTTPS (Render does this automatically)

## Next Steps

- Set up a custom domain (optional)
- Configure email for contact forms
- Set up database backups
- Monitor your application performance 