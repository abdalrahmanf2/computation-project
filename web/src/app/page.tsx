"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import { PredictForm } from "./predict-form";
import { useState } from "react";
import { cn } from "~/lib/utils";

export interface Prediction {
  win: boolean;
  probability: number;
  prediction: number;
}

export default function HomePage() {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  console.log(prediction);

  return (
    <main className="flex h-screen w-screen flex-col items-center justify-center gap-4">
      {prediction && (
        <Card
          className={cn(
            "w-full max-w-2xl border-2 shadow-none",
            prediction.win
              ? "border-green-400 bg-green-400/10"
              : "border-red-400 bg-red-400/10",
          )}
        >
          <CardHeader>
            <CardTitle
              className={cn(
                "text-center text-2xl",
                prediction.win ? "text-green-600" : "text-red-600",
              )}
            >
              {prediction.win ? "Wins" : "Losses"}
            </CardTitle>
            <CardDescription className="text-center">
              <p className="text-sm text-gray-600">
                {prediction.win
                  ? `Winning probability: ${Math.round(prediction?.probability * 100)}%`
                  : `Losing probability: ${Math.round((1 - prediction?.probability) * 100)}%`}
              </p>
            </CardDescription>
          </CardHeader>
        </Card>
      )}

      <Card className="w-full max-w-2xl shadow-none">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">
            Predict Game Outcome
          </CardTitle>
          <CardDescription>
            Predict the outcome of a game based on the features provided.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <PredictForm setPrediction={setPrediction} />
        </CardContent>
      </Card>
    </main>
  );
}
