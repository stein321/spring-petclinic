@Library('ldop-shared-library') _
pipeline {
    agent none
    stages {
       stage('Build') {
           agent {
               docker {
                   image 'maven:3.5.0'
               }
           }
           steps {
                   sh 'mvn clean install -DskipTests=true -B'
           }
       }
       stage('Build with branchname and push') {
             agent any
             steps {
                 sh "docker build -t stein321/petclinic-tomcat:${env.BRANCH_NAME} ."
                //  sh 'docker push  stein321/petclinic-tomcat:${env.BRANCH_NAME}'
             }
       }
       stage('Build container with version') {
           when { branch 'poc-pipeline'}
            agent any
           steps {
            //    script {
            //        sh "docker inspect stein321/petclinic-tomcat:${env.BRANCH_NAME} > containerMetaData.json"
            //         def metaData = readJSON file: "containerMetaData.json"
            //         println metaData
            //         def version = metaData[0].ContainerConfig.Labels.version
            //         println version
            //    }
                // getVersionFromContainer("stein321/petclinic-tomcat:${env.BRANCH_NAME}")
                sh "docker build -t stein321/petclinic-tomcat:${getVersionFromContainer("stein321/petclinic-tomcat:${env.BRANCH_NAME}")} ."
           }
       }
   }
}
