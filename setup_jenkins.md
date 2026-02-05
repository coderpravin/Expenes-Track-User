# Jenkins & SonarQube Setup Guide

This guide details how to spin up your local CI/CD infrastructure and run your first pipeline.

## 1. Start the Infrastructure

Run the following command in your terminal (`ExpenseTracker_Mech/Expenes-Track-User` directory):

```powershell
docker-compose up -d
```

This starts:
-   **Jenkins**: [http://localhost:8080](http://localhost:8080)
-   **SonarQube**: [http://localhost:9000](http://localhost:9000)

## 2. Configure SonarQube

1.  Open [http://localhost:9000](http://localhost:9000).
2.  Login with `admin` / `admin` (Change password when prompted).
3.  **Create a Token**:
    -   Go to **User > My Account > Security**.
    -   Generate a token named `jenkins-token`. **Copy this token**.
4.  **Create a Webhook** (Optional but recommended):
    -   Go to **Administration > Configuration > Webhooks**.
    -   Create a webhook pointing to your Jenkins (if applicable), or skip for now.

## 3. Configure Jenkins

1.  Open [http://localhost:8080](http://localhost:8080).
2.  **Unlock Jenkins**:
    -   Run `docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword` in your terminal to get the password.
3.  **Install Plugins**:
    -   Select "Install suggested plugins".
    -   Once installed, go to **Manage Jenkins > Plugins > Available Plugins**.
    -   Search for and install:
        -   **SonarQube Scanner**
        -   **Docker Pipeline**
        -   **Docker**
4.  **Configure SonarQube in Jenkins**:
    -   Go to **Manage Jenkins > System**.
    -   Scroll to **SonarQube servers**.
    -   Click **Add SonarQube**.
    -   **Name**: `sonar-server` (Must match `Jenkinsfile`!).
    -   **Server URL**: `http://sonarqube:9000` (Note: Use container name `sonarqube`, not `localhost`).
    -   **Server authentication token**: Add the token you copied from SonarQube as a "Secret Text" credential.
5.  **Configure SonarQube Scanner Tool**:
    -   Go to **Manage Jenkins > Tools**.
    -   Scroll to **SonarQube Scanner installations**.
    -   Click **Add SonarQube Scanner**.
    -   **Name**: `SonarScanner` (This EXACLTY matches the Jenkinsfile).
    -   **Install automatically**: Checked.
    -   Select "Install from Maven Central".
    -   Click **Save**.
6.  **Configure Docker Tool** (Optional but good practice):
    -   Go to **Manage Jenkins > Tools**.
    -   Ensure "Docker" is configured or available in path. Usually, the "Docker Pipeline" plugin handles the node block.

## 4. Create the Pipeline Job

1.  Click **New Item** on dashboard.
2.  Enter name: `ExpenseTracker-CI`.
3.  Select **Pipeline** and click OK.
4.  Scroll to **Pipeline** section.
5.  **Definition**: "Pipeline script from SCM".
6.  **SCM**: Git.
7.  **Repository URL**: Path to your local git repo or GitHub URL (e.g., `https://github.com/your/repo.git`).
    -   *Tip: If testing locally without pushing, you might need to mount your local dir or use a file path, but GitHub is easiest.*
8.  **Script Path**: `Jenkinsfile`.
9.  Click **Save**.

## 5. Run it!

1.  Click **Build Now**.
2.  Open the build and click **Pipeline Steps** or **Console Output** to watch it happen.
3.  Once finished, check the **SonarQube** link on the project dashboard to see your code quality report.

## Troubleshooting

-   **Docker Permission Denied**: If Jenkins fails to run docker commands, ensure line 15 in `docker-compose.yml` (`//var/run/docker.sock...`) is working for your OS. On Windows, the double slash `//` is often needed for Git Bash/MinGW, but sometimes single `/` works for PowerShell.
-   **Line Endings**: If scripts fail with "command not found" or weird characters, ensure `.gitattributes` is present and you've re-cloned or re-checked out the files.
