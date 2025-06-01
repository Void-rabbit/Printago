#ifndef SETTINGSPAGE_H
#define SETTINGSPAGE_H

#include <QWidget>

// Forward declarations
class QLabel;
class QListWidget;
class QPushButton;
class QVBoxLayout;
class QHBoxLayout;
class QTabWidget;
class QGroupBox; // Though QGroupBox is listed, it's not used in the plan. Will omit for now unless needed.

class IDataService; // Forward declaration

class SettingsPage : public QWidget
{
    Q_OBJECT

public:
    explicit SettingsPage(IDataService* dataService, QWidget *parent = nullptr);

private slots:
    void refreshParts();
    void refreshProfiles();
    // Add slots for button states if needed, similar to JobManagementPage

private:
    QWidget* createPartsTab();
    QWidget* createProfilesTab();

    IDataService* m_dataService;
    QTabWidget *tabWidget;

    // For Parts Tab
    QWidget *partsTab; // This will be the widget returned by createPartsTab
    QListWidget *partsListWidget;
    QPushButton *addPartButton;
    QPushButton *editPartButton;
    QPushButton *deletePartButton;

    // For Profiles Tab
    QWidget *profilesTab; // This will be the widget returned by createProfilesTab
    QListWidget *profilesListWidget;
    QPushButton *addProfileButton;
    QPushButton *editProfileButton;
    QPushButton *deleteProfileButton;
};

#endif // SETTINGSPAGE_H
