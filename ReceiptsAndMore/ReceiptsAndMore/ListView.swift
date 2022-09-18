//
//  ListView.swift
//  ReceiptsAndMore
//
//  Created by Maddie Estey on 9/18/22.
//

import SwiftUI

struct ListView: View {
    var body: some View {
        VStack {
            Text("Receipts for 2022")
                .bold()
                .background(
                    Rectangle()
                        .fill(.blue)
                        .frame(width: 400, height: 80))
                .foregroundColor(.white)
                .offset(y: -200)
        
            /*Rectangle()
                .fill(.blue)
                .frame(width: 400, height: 60)
                .offset(y: -210)
             */
            HStack {
                
            }
            Button {
                //
            } label: {
                Text("Add Receipt")
                    .bold()
                    .frame(width: 300, height: 35)
                    .background(
                        RoundedRectangle(cornerRadius: 10, style: .continuous)
                            .fill(.linearGradient(colors: [.blue, .green], startPoint: .topLeading, endPoint: .bottomTrailing)))
                    .foregroundColor(.white)
                    .offset(y: 230)
            }
            
            Button {
                //
            } label: {
                Text("Upload Credit Statement")
                    .bold()
                    .frame(width: 300, height: 35)
                    .background(
                        RoundedRectangle(cornerRadius: 10, style: .continuous)
                            .fill(.linearGradient(colors: [.blue, .green], startPoint: .topLeading, endPoint: .bottomTrailing)))
                    .foregroundColor(.white)
                    .offset(y: 220)
            }
            .padding()
        }
        
    }
}

struct ListView_Previews: PreviewProvider {
    static var previews: some View {
        ListView()
    }
}
