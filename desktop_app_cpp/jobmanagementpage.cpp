#include "jobmanagementpage.h"

#include <QLabel>
#include <QListWidget>
#include <QListWidgetItem>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFont> // For styling title
#include <QDebug> // For messages

#include "Printago/Agents/IDataService.h" // Full include

JobManagementPage::JobManagementPage(IDataService* dataService, QWidget *parent)
    : QWidget(parent), m_dataService(dataService)
{
    Q_ASSERT(m_dataService != nullptr);
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setAlignment(Qt::AlignTop);

    // Title
    titleLabel = new QLabel("Print Job Management", this);
    QFont titleFont = titleLabel->font();
    titleFont.setPointSize(16);
    titleFont.setBold(true);
    titleLabel->setFont(titleFont);
    titleLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(titleLabel, 0, Qt::AlignTop);
    mainLayout->addSpacing(10);

    // Button Layout
    QHBoxLayout *controlsLayout = new QHBoxLayout(); // Renamed for clarity
    startJobButton = new QPushButton("Start New Job", this);
    pauseJobButton = new QPushButton("Pause Selected", this);
    cancelJobButton = new QPushButton("Cancel Selected", this);
    refreshJobsButton = new QPushButton("Refresh List", this); // Added refresh button
    connect(refreshJobsButton, &QPushButton::clicked, this, &JobManagementPage::refreshJobs);

    controlsLayout->addWidget(startJobButton);
    controlsLayout->addSpacing(10);
    controlsLayout->addWidget(pauseJobButton);
    controlsLayout->addSpacing(10);
    controlsLayout->addWidget(cancelJobButton);
    controlsLayout->addStretch();
    controlsLayout->addWidget(refreshJobsButton); // Add refresh button to layout
    mainLayout->addLayout(controlsLayout);
    mainLayout->addSpacing(10);

    // Job List Widget
    jobListWidget = new QListWidget(this);
    mainLayout->addWidget(jobListWidget, 1); // Allow list to stretch

    // Connect selection change to update button states
    connect(jobListWidget, &QListWidget::itemSelectionChanged, this, &JobManagementPage::updateButtonStates);

    // Initial load of jobs and button states
    refreshJobs(); // Changed from loadMockJobs
    // updateButtonStates(); // Called by refreshJobs after data is loaded

    setLayout(mainLayout);
}

void JobManagementPage::refreshJobs()
{
    if (!m_dataService) {
        qWarning("JobManagementPage: Data service is not available.");
        jobListWidget->clear();
        jobListWidget->addItem("Error: Data service unavailable.");
        updateButtonStates();
        return;
    }

    // jobListWidget->clear();
    // jobListWidget->addItem("Loading jobs..."); // Optional loading state

    m_dataService->fetchPrintJobs(
        [this](bool success, const QList<QVariantMap>& jobs, const QString& message) {
            jobListWidget->clear();
            if (success) {
                if (jobs.isEmpty()) {
                    jobListWidget->addItem("No print jobs found.");
                } else {
                    for (const QVariantMap& jobMap : jobs) {
                        QString itemText = QString("%1 - %2 (Printer: %3)")
                                               .arg(jobMap["name"].toString())
                                               .arg(jobMap["status"].toString())
                                               .arg(jobMap["printer_id"].toString()); // Assuming printer_id is enough for now
                        QListWidgetItem* item = new QListWidgetItem(itemText);
                        item->setData(Qt::UserRole, jobMap["status"].toString()); // Store status for button logic

                        // Example: Color coding based on status
                        QString status = jobMap["status"].toString().toLower();
                        if (status.contains("printing")) item->setForeground(Qt::blue);
                        else if (status.contains("queued")) item->setForeground(Qt::darkYellow);
                        else if (status.contains("completed")) item->setForeground(Qt::darkGreen);
                        else if (status.contains("failed")) item->setForeground(Qt::red);
                        else if (status.contains("offline")) item->setForeground(Qt::gray);

                        jobListWidget->addItem(item);
                    }
                }
                qDebug() << "JobManagementPage: Jobs loaded -" << message;
            } else {
                jobListWidget->addItem(QString("Failed to load jobs: %1").arg(message));
                qWarning() << "JobManagementPage: Failed to load jobs -" << message;
            }
            updateButtonStates(); // Update buttons after list is populated
        });
}

void JobManagementPage::updateButtonStates()
{
    bool itemSelected = !jobListWidget->selectedItems().isEmpty();
    QString currentStatus;

    if (itemSelected) {
        currentStatus = jobListWidget->selectedItems().first()->data(Qt::UserRole).toString();
    }

    pauseJobButton->setEnabled(itemSelected && (currentStatus == "Printing" || currentStatus == "Queued"));
    cancelJobButton->setEnabled(itemSelected && (currentStatus == "Printing" || currentStatus == "Queued" || currentStatus == "Paused")); // Assuming Paused state exists

    // Logic for startJobButton (usually always enabled or depends on other factors)
    startJobButton->setEnabled(true);
}
