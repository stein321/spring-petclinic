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
       stage('Build latest') {
             agent any
             steps {
                 sh 'docker build -t stein321/petclinic-tomcat:latest .'
             }
       }
       stage('push') {
           agent any
           steps {
               sh 'docker build -t stein321/petclinic-tomcat:latest .'
           }
       }
       stage('get version') {
        //    when { branch 'master' }
           agent any
           steps {
               sh "docker inspect stein321/petclinic-tomcat:latest > containerMetaData.json"
               script {
                   def containerMetaData = readJSON file: 'containerMetaData.json'
                   println containerMetaData[0].ContainerConfig.Labels.version.split(" ")[1]
               }
           }
       }
    //    stage('') {
    //        when { branch 'master'}
    //        agent any
    //        environment {
    //            version = getVersionFromContainer()
    //        }
    //        steps {
    //            sh "docker build -t stein321/petclinic-tomcat:${version}"
    //        }
    //    }

    }
}
