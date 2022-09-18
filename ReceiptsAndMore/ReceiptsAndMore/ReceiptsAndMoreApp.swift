//
//  ReceiptsAndMoreApp.swift
//  ReceiptsAndMore
//
//  Created by MacBookPro on 2022/9/16.
//

import SwiftUI
import Firebase
import FirebaseCore
import FirebaseAuth

class AppDelegate: NSObject, UIApplicationDelegate {
  func application(_ application: UIApplication,
                   didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
      if(FirebaseApp.app() == nil){
          FirebaseApp.configure()
      }

    return true
  }
}

@main
struct ReceiptsAndMoreApp: App {
    //@StateObject var dataManager = DataManager()
    init() {
        FirebaseApp.configure()
    }
    
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate
    var body: some Scene {
        WindowGroup {
            NavigationView {
                //ContentView()
                ListView()
            }
        }
    }
}
