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
            agent {
                docker { 
                    image 'python:3.10' 
                    // Reuse the workspace so we don't redownload everything if possible, 
                    // or just run it clean. 
                    // For this pipeline, we will build the distinct Docker image defined in Dockerfile
                    // But to keep it simple first, let's use the Dockerfile we created.
                    reuseNode true
                }
            }
            steps {
                // We actually want to build the image from our Dockerfile
                script {
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
