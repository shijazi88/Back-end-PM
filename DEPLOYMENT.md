# Deployment Guide for Back-end-PM

This guide covers deploying the Back-end-PM Django application to DigitalOcean App Platform.

## Pre-deployment Changes Made

### 1. Fixed Dependencies

- Updated PyTorch versions to remove CPU-specific suffixes that were causing build failures
- Changed from `torch==2.8.0`, `torchaudio==2.8.0+cpu`, `torchvision==0.23.0+cpu`
- To: `torch==2.4.0`, `torchaudio==2.4.0`, `torchvision==0.19.0`
- Added production dependencies: `gunicorn`, `whitenoise`
- Removed PostgreSQL dependencies: `psycopg2-binary`, `dj-database-url`

### 2. Created Production Settings

- Created `agri_project/settings_production.py` with:
  - Environment variable configuration
  - SQLite database configuration (simpler than PostgreSQL)
  - Static files handling with WhiteNoise
  - Security settings for production
  - CORS configuration

### 3. Added Deployment Files

- `.do/app.yaml`: DigitalOcean App Platform configuration
- `Dockerfile`: Container configuration
- `docker-compose.yml`: Local testing setup
- `Procfile`: Process configuration
- `start.sh`: Startup script

## DigitalOcean App Platform Deployment

### Method 1: Using App Spec (Recommended)

1. **Push your code to GitHub**

   ```bash
   git add .
   git commit -m "Prepare for DigitalOcean deployment"
   git push origin main
   ```

2. **Create App in DigitalOcean**

   - Go to DigitalOcean Dashboard → Apps
   - Click "Create App"
   - Connect your GitHub repository: `shijazi88/Back-end-PM`
   - DigitalOcean will detect the `.do/app.yaml` file

3. **Set Environment Variables**
   In the DigitalOcean App Platform dashboard, add these environment variables:
   ```
   SECRET_KEY=your-secret-key-here
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
   SENDGRID_API_KEY=your-sendgrid-api-key
   DEFAULT_FROM_EMAIL=your-email@domain.com
   FRONTEND_URL=https://your-frontend-domain.com
   ```

### Method 2: Manual Configuration

1. **Create New App**

   - Choose "GitHub" as source
   - Select repository: `shijazi88/Back-end-PM`
   - Branch: `main`

2. **Configure Service**

   - Name: `web`
   - Environment: Python
   - Build Command: (leave default)
   - Run Command: `gunicorn --worker-tmp-dir /dev/shm agri_project.wsgi`

3. **Database Configuration**

   - No external database needed (using SQLite)
   - Database file will be created automatically

4. **Environment Variables**
   Add the same environment variables as listed above.

## Local Testing with Docker

1. **Build and run locally**

   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Application: http://localhost:8000
   - Database: SQLite file (db.sqlite3)

## Important Notes

### Security Considerations

- Change the `SECRET_KEY` in production
- Set `DEBUG=False` in production (already configured)
- Update `ALLOWED_HOSTS` with your actual domain
- Configure proper CORS origins

### Database Migration

- The app will automatically run migrations on deployment
- Make sure your database is properly configured

### Static Files

- WhiteNoise is configured to serve static files
- Run `python manage.py collectstatic` during deployment

### Model Files

According to the original README, you need to:

1. Download model files from: https://drive.google.com/drive/u/0/folders/1Qpr4pNgK11VXIwZ5JZ0M5ctDANu7k2vI
2. Place them in a `model_files/` directory
3. This step may need to be done manually after deployment

## Troubleshooting

### Common Issues

1. **Build Failures**

   - Check that all dependencies in `requirements.txt` are compatible
   - Ensure Python version compatibility (using Python 3.11)

2. **Database Issues**

   - SQLite database will be created automatically
   - Ensure the application has write permissions to the filesystem

3. **Static Files Not Loading**
   - Ensure `STATIC_ROOT` is properly configured
   - Verify WhiteNoise is in `MIDDLEWARE`

### Logs

Check application logs in DigitalOcean dashboard:

- Go to your app → Runtime Logs
- Look for any error messages during startup

## Post-Deployment Steps

1. **Default Superuser**
   The application automatically creates a default superuser on first deployment:

   - **Email**: `maiizainelabdeen@gmail.com`
   - **Password**: `Mm22112001*`
   - **Full Name**: `Mai Zain Elabdeen`

   You can also manually create the default superuser using:

   ```bash
   python manage.py create_default_superuser
   ```

2. **Upload Model Files**
   If needed, upload the model files to the `model_files/` directory

3. **Test API Endpoints**
   Verify that your API endpoints are working correctly

4. **Configure Domain**
   Set up your custom domain if needed

## Environment Variables Reference

| Variable                 | Description                       | Required          |
| ------------------------ | --------------------------------- | ----------------- |
| `SECRET_KEY`             | Django secret key                 | Yes               |
| `DEBUG`                  | Debug mode (False for production) | Yes               |
| `DATABASE_URL`           | Database connection string        | No (using SQLite) |
| `ALLOWED_HOSTS`          | Allowed hostnames                 | Yes (auto-set)    |
| `CORS_ALLOWED_ORIGINS`   | CORS allowed origins              | Yes               |
| `STRIPE_SECRET_KEY`      | Stripe secret key                 | Yes               |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key            | Yes               |
| `SENDGRID_API_KEY`       | SendGrid API key                  | Optional          |
| `DEFAULT_FROM_EMAIL`     | Default email sender              | Optional          |
| `FRONTEND_URL`           | Frontend application URL          | Yes               |
