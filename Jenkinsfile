pipeline {
    agent any
    stages {
        stage('Set up Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python --version
                '''
            }
        }
        stage('Install dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install black flake8 pytest
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                '''
            }
        }
        stage('Check formatting with black') {
            steps {
                sh '''
                    . venv/bin/activate
                    black --verbose --check ./*.py
                '''
            }
        }
        stage('Lint with flake8') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 --verbose ./*.py
                '''
            }
        }
        stage('Test with pytest') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --verbose ./test*.py
                '''
            }
        }
        stage('Create and deliver the artifact') {
            steps {
                sh '''
                    zip main-${BUILD_NUMBER}.zip main.py
                '''

                archiveArtifacts artifacts: '*.zip', fingerprint: true
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
