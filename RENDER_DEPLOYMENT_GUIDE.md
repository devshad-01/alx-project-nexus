# RENDER DEPLOYMENT SETUP GUIDE
# ===============================

## Step 1: Create PostgreSQL Database on Render

1. Go to your Render Dashboard: https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Database Details:
   - Name: `ecommerce-db` (or any name you prefer)
   - Database: `ecommerce_db`
   - User: `ecommerce_user`
   - Region: Choose closest to your location
   - Plan: Free (for testing) or paid (for production)
4. Click "Create Database"
5. Once created, copy the "External Database URL" - this is your DATABASE_URL

## Step 2: Set Environment Variables in Render Web Service

Go to your web service → Environment tab and add these variables:

### REQUIRED Variables:
```
SECRET_KEY=o)uv+t84%*m8pl6r5imu9!mb$x&vp)q_53ed1)07+2h3o9+ymw
DATABASE_URL=postgresql://ecommerce_user:password@hostname:port/ecommerce_db
ALLOWED_HOSTS=your-app-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com
DEBUG=False
```

### OPTIONAL Variables:
```
REDIS_URL=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
USE_S3_STORAGE=False
```

## Step 3: Replace Placeholders

Replace these placeholders with your actual values:
- `your-app-name` → Your actual Render web service name
- `DATABASE_URL` → The External Database URL from Step 1
- Email settings → Your email credentials (if needed)

## Step 4: Deploy

After setting the environment variables:
1. Your app will automatically redeploy
2. Database migrations will run
3. Your API will be live at: https://your-app-name.onrender.com

## Step 5: Test Your Deployment

Test these endpoints:
- API Root: https://your-app-name.onrender.com/api/
- API Documentation: https://your-app-name.onrender.com/api/docs/
- Admin Panel: https://your-app-name.onrender.com/admin/

## Troubleshooting

If deployment fails:
1. Check the deployment logs in Render dashboard
2. Verify all REQUIRED environment variables are set
3. Ensure DATABASE_URL is correct and database is accessible
4. Check that ALLOWED_HOSTS includes your Render domain

## Creating a Superuser (After Successful Deployment)

To access the admin panel, you'll need to create a superuser:
1. Go to Render dashboard → Your web service → Shell tab
2. Run: `python manage.py createsuperuser`
3. Follow the prompts to create admin user
4. Access admin at: https://your-app-name.onrender.com/admin/
