// inference_api.cpp

#include <iostream>
#include <string>

using namespace std;

// Simulated logic
string classify_text(const string &text) {
    if (text.find("fake") != string::npos || text.length() < 30)
        return "Fake";
    return "Real";
}

int main() {
    int choice;
    cout << "Choose type to test:\n1. Text\n2. Audio\n3. Video\nChoice: ";
    cin >> choice;
    cin.ignore();

    if (choice == 1) {
        string text;
        cout << "Enter text content: ";
        getline(cin, text);
        cout << "Result: " << classify_text(text) << endl;
    }
    else if (choice == 2) {
        system("./audio_analyzer");
    }
    else if (choice == 3) {
        system("./video_checker");
    }
    else {
        cout << "Invalid choice.\n";
    }

    return 0;
}
