pipeline {
    agent any

    environment {
        // Ensure scripts use a consistent path
        PATH = "$PATH:/usr/local/bin"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Install Dependencies') {
            steps {
                script {
                    // Build the Docker image on the Jenkins agent (which has Docker CLI)
                    dockerImage = docker.build("expense-tracker-test")
                }
            }
        }

        stage('Static Code Analysis (SonarQube)') {
            steps {
                script {
                    // Requires 'SonarQube Scanner' plugin in Jenkins
                    // and a SonarQube server configured with name 'sonar-server'
                    def scannerHome = tool 'SonarScanner' 
                    withSonarQubeEnv('sonar-server') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    // Requires SonarQube Webhook to be configured in SonarQube pointing to Jenkins
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Security Scan (Dependencies)') {
            steps {
                // Run the docker image we built to check dependencies inside it
                script {
                    dockerImage.inside {
                        sh 'pip install safety'
                        sh 'safety check -r requirements.txt --continue-on-error'
                    }
                }
            }
        }

        stage('Test') {
             steps {
                script {
                    dockerImage.inside {
                        sh 'python project/manage.py check'
                        sh 'python project/manage.py test'
                    }
                }
            }
        }
    }
}
