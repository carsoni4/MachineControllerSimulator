#include "mainwindow.h"
#include "./ui_mainwindow.h"

#include <QtNetwork/QNetworkRequest>
#include <QtNetwork/QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <QUrl>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , networkManager(new QNetworkAccessManager(this))
{
    ui->setupUi(this);

    connect(ui->btnStartEngine, &QPushButton::clicked, this, [this](){
        sendCommand("ENGINE_START", [this](const QJsonObject response){
            QString status = response["status"].toString();
            if (status == "OK"){
                ui->engineRunningLabel->setText("Engine ON");
            }
        });
    });

    connect(ui->btnStopEngine, &QPushButton::clicked, this, [this](){
        sendCommand("ENGINE_STOP", [this](const QJsonObject response){
            QString status = response["status"].toString();
            if (status == "OK"){
                ui->engineRunningLabel->setText("Engine OFF");
                ui->speedValue->display(0);
            }
        });
    });

    connect(ui->speedDial, &QDial::sliderReleased, this, [this]() {
        int speed = ui->speedDial->value();

        sendCommand("ENGINE_SPEED_SET " + QString::number(speed), [this, speed](const QJsonObject &response){
            QString status = response["status"].toString();

            if (status == "OK") {
                    ui->speedValue->display(speed);
                }
            }
        );
    });

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::sendCommand(const QString &command, std::function<void(const QJsonObject &)> onResponse)
{
    QUrl url("http://127.0.0.1:8000/commands/send");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject body;
    body["command"] = command;

    QByteArray data = QJsonDocument(body).toJson();

    QNetworkReply *reply = networkManager->post(request, data);

    connect(reply, &QNetworkReply::finished, this, [this, reply, command, onResponse]() {
        if (reply->error() != QNetworkReply::NoError) {
            QJsonObject errorResponse;
            errorResponse["status"] = "ERROR";
            errorResponse["message"] = reply->errorString();

            ui->txtLog->append("Network error sending: " + command);
            ui->txtLog->append(reply->errorString());

            onResponse(errorResponse);

            reply->deleteLater();
            return;
        }

        QByteArray responseData = reply->readAll();
        QJsonDocument responseJson = QJsonDocument::fromJson(responseData);
        QJsonObject responseObject = responseJson.object();

        QString status = responseObject["status"].toString();
        QString message = responseObject["message"].toString();

        ui->txtLog->append("Sent command: " + command);
        ui->txtLog->append(message);

        onResponse(responseObject);

        reply->deleteLater();
    });
}
