//
//  NewReceipt.swift
//  ReceiptsAndMore
//
//  Created by Maddie Estey on 9/17/22.
//

import SwiftUI

struct NewReceipt: View {
    @EnvironmentObject var dataManager: DataManager
    @State private var newreceipt = ""
    
    var body: some View {
        VStack {
            TextField("Receipt", text: $newreceipt)
            
            Button {
                dataManager.addReceipt(company: newreceipt)
            } label: {
                Text("Save")
            }
        }
        .padding()
            
    }
}

struct NewReceipt_Previews: PreviewProvider {
    static var previews: some View {
        NewReceipt()
    }
}
