//
//  DataManager.swift
//  ReceiptsAndMore
//
//  Created by Maddie Estey on 9/17/22.
//

import SwiftUI
import Firebase
import FirebaseCore
import FirebaseFirestore

class DataManager: ObservableObject {
    @Published var dogs: [Page] = []
    
    
    
    init() {
        fetchStuff()
    }
    
    func fetchStuff() {
        dogs.removeAll()
        let db = Firestore.firestore()
        let ref = db.collection("Info")
        ref.getDocuments { snapshot, error in
            guard error == nil else {
                print(error!.localizedDescription)
                return
            }
            
            if let snapshot = snapshot {
                for document in snapshot.documents {
                    let data = document.data()
                    
                    let id = data["id"] as? String ?? ""
                    
                    let dog = Page(id: id, company: company)
                    self.dogs.append(dog)
                }
            }
        }
    }
    
    func addReceipt(company: String) {
        let db = Firestore.firestore()
        let ref = db.collection("Dogs").document(company)
        ref.setData(["company": company, "id" : 10]) { error in
            if let error = error {
                print(error.localizedDescription)
            }
        }
    }
}
