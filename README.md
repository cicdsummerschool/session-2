# session-2

## Comparing CI/CD framework configurations

This repository contains a Python script that prints "Hello, World!" to the console and an associated test suite.

The pipeline for the project is made up of a few steps that:

- Checkout the code
- Install dependencies
- Link the code
- Run a test suite
- Package the code as a zip file

The pipeline has been implemented in three different CI/CD frameworks:

- [GitHub Actions (YAML)](./.github/workflows/python-app.yml)
- [Jenkins (Groovy)](./Jenkinsfile)
- [TeamCity (Kotlin)](./.teamcity/teamcity.kts)

**Compare the configurations of the three frameworks to identify similarities and differences.**

## GitHub Actions

- [GitHub Actions Configuration](.github/workflows/python-app.yml)

```
name: Integration and Delivery Workflow

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read

jobs:
  integration:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python 3.10
      uses: actions/setup-python@v5
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Check formatting with black
      run: black --verbose --check ./*.py

    - name: Lint with flake8
      run: flake8 --verbose ./*.py

    - name: Test with pytest
      run: pytest --verbose  ./test*.py

  delivery:
    runs-on: ubuntu-latest
    needs: integration

    steps:
    - uses: actions/checkout@v4

    - name: Create and deliver the artifact
      uses: actions/upload-artifact@v4
      with:
        name: main-${{ github.sha }}
        path: ./main.py

```

## Jenkins

- [Jenkins Configuration](Jenkinsfile)

```
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
```

## TeamCity

- [TeamCity Configuration](.teamcity/teamcity.kts)

```
package _Self.buildTypes

import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.buildSteps.python
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs

object Build : BuildType({
    name = "Build"

    artifactRules = "*.zip"

    vcs {
        root(HttpsGithubComCicdsummerschoolSession2gitRefsHeadsMain)
    }
steps {
    script {
        name = "Install dependencies"
        id = "Install_dependencies"
        scriptContent = """
            python -m pip install --upgrade pip
            pip install black flake8
        """.trimIndent()
    }
    script {
        name = "Check formatting with black"
        id = "Install_dependencies"
        scriptContent = """
            black --verbose --check ./*.py
        """.trimIndent()
    }
    script {
        name = "Lint with flake8"
        id = "Install_dependencies"
        scriptContent = """
            flake8 --verbose ./*.py
        """.trimIndent()
    }
    python {
        name = "Run Pytest"
        id = "python_runner_0"
        command = pytest {
        }
    }
    script {
        name = "Create and deliver the artifact"
        id = "Create_and_deliver_the_artifact"
        scriptContent = "zip zip main-${'$'}{BUILD_VCS_NUMBER}.zip main.py"
    }
}
    triggers {
        vcs {
        }
    }

    features {
        perfmon {
        }
    }
})
```
