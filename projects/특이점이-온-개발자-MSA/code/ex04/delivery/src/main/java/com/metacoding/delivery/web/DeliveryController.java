package com.metacoding.delivery.web;

import com.metacoding.delivery.usecase.*;
import org.springframework.http.ResponseEntity;
import com.metacoding.delivery.core.util.Resp;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/deliveries")
public class DeliveryController {
    private final GetDeliveryUseCase getDeliveryUseCase;
    private final CompleteDeliveryUseCase completeDeliveryUseCase;

    @GetMapping("/{deliveryId}")
    public ResponseEntity<?> getDelivery(@PathVariable("deliveryId") int deliveryId) {
        return Resp.ok(getDeliveryUseCase.findById(deliveryId));
    }

    @PutMapping("/{deliveryId}/complete")
    public ResponseEntity<?> completeDelivery(@PathVariable("deliveryId") int deliveryId) {
        return Resp.ok(completeDeliveryUseCase.completeDelivery(deliveryId));
    }
}
